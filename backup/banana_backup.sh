#!/bin/bash

# Create backups of GitLab instances
# 1. Trigger a backup on the GitLab instance running inside a
#    specified container
# 2. Download the backup and extra configuration files that are not included
#    in the backup by default
# 3. Check file integrity
# 4. Remove remote backups
#
# Authored by: Bevilacqua Joey, Gianmarco De Vita

CONFIG_PATH="$(pwd)/backups.conf"
HAS_TPUT=$(which tput)
VERBOSE=false

printError() {
    if [[ $HAS_TPUT ]]; then
        echo "$(tput setaf 1)${1}$(tput sgr reset)"
    else
        echo "Error:\t$1"
    fi
}

printSuccess() {
    if [[ $HAS_TPUT ]]; then
        echo "$(tput setaf 2)${1}$(tput sgr reset)"
    else
        echo "$1"
    fi
}

printInfo() {
    if [[ $VERBOSE ]]; then
        echo "$1"
    fi
}

getShaExec() {
    local sha_exec=$(which sha512sum)
    if [[ $sha_exec ]]; then
        printInfo "Using $sha_exec as shasum executable"
        return $sha_exec
    fi

    # Probably MacOS
    sha_exec=$(which shasum)
    if [[ $sha_exec ]]; then
        printInfo "Using $sha_exec as shasum executable"
        return "${sha_exec} -a512"
    fi

    printError "Failed to find a shasum executable"
    return 1
}

# 1. Setup
if [[ ! -f $CONFIG_PATH ]]; then
    printError "Missing config file ${CONFIG_PATH}"
    exit 1
fi
source $CONFIG_PATH

# 2. Check if container is running
printInfo "Connecting to $CONTAINER_NAME ..."
if [[ "$(which docker)" == 0 ]]; then
    printError "Couldn't find a docker executable, aborting ..."
    exit 2
fi
if [[ "$(docker container inspect -f '{{.State.Running}}' $CONTAINER_NAME)" != "true" ]]; then
    printError "The container $CONTAINER_NAME is not running, aborting..."
    exit 2
fi


# 3. Create the backup remotely
echo "Creating backup ..."
docker exec "$CONTAINER_NAME" $EXEC_CREATE_BACKUP
if [[ $? != 0 ]]; then
    echo "Failure: couldn't create a backup!"
    exit 3
fi
printSuccess "Backup created successfully!"

# 4. Download the backup files
echo "Downloading files ..."
MOST_RECENT_BACKUP="$(docker exec $CONTAINER_NAME ls -t $REMOTE_PATH | head -n1)"
BACKUP_NAME="backup_$(date '+%Y-%m-%d_%H-%M-%S')"
mkdir -p "${LOCAL_PATH}/${BACKUP_NAME}"
if [[ $? != 0 ]]; then
    printError "Couldn't prepare for backup..."
    exit 4
fi

docker cp "${CONTAINER_NAME}:${REMOTE_PATH}/${MOST_RECENT_BACKUP}" "${LOCAL_PATH}/${BACKUP_NAME}/"
if [[ $? != 0 ]]; then
    printError "Failed to download the backup from the container"
    exit 4
fi

for f in ${REMOTE_EXTRA_FILES[@]}; do
    printInfo "Downloading ${f} from container ..."
    docker cp "${CONTAINER_NAME}:${f}" "${LOCAL_PATH}/${BACKUP_NAME}/"
    if [[ $? != 0 ]]; then
        printError "Failed to download extra file $f"
        exit 4
    fi
done
printSuccess "Backup downloaded successfully!"

# 6. Check integrity
SHA_EXEC=$(getShaExec())
echo "Checking integrity ..."
REMOTE_HASH=$(docker exec "$CONTAINER_NAME" sha512sum "${REMOTE_PATH}/${MOST_RECENT_BACKUP}" | cut -d ' ' -f1)
LOCAL_HASH=$($SHA_EXEC "${LOCAL_PATH}/${BACKUP_NAME}/${MOST_RECENT_BACKUP}" | cut -d ' ' -f1)
if [[ "$REMOTE_HASH" != "$LOCAL_HASH" ]]; then
    printError "Integrity check failed, aborting..."
    exit 6
fi
printSuccess "Integrity check passed!"

# 7. Zip it
echo "Compressing backup ..."
ZIP_BACKUP="${BACKUP_NAME}.zip"
zip -r "${LOCAL_PATH}/${ZIP_BACKUP}" "${LOCAL_PATH}/${BACKUP_NAME}"
if [[ $? != 0 ]]; then
    printError "Failed to compress the backup"
    exit 7
fi
# Save sha512 of our backup
$SHA_EXEC "${LOCAL_PATH}/${ZIP_BACKUP}" > "${LOCAL_PATH}/${ZIP_BACKUP}.sha512"
if [[ $? != 0 ]]; then
    printError "Failed to compute hash of the zip";
    exit 7
fi

# 8. Remove tmp data
echo "Cleaning up ..."
docker exec "$CONTAINER_NAME" rm "${REMOTE_PATH}/${MOST_RECENT_BACKUP}"
if [[ $? != 0 ]]; then
    printError "Failed to remove remote tmp backup data";
    exit 8
fi
rm -r "${LOCAL_PATH}/${BACKUP_NAME}"
if [[ $? != 0 ]]; then
    printError "Failed to remove remote tmp backup data";
    exit 8
fi

printSuccess "Done!"
