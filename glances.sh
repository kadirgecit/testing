#!/usr/bin/env bash

# Execute a command as root (or sudo)
do_with_root() {
    # already root? "Just do it" (tm).
    if [[ `whoami` = 'root' ]]; then
        $@
    elif [[ -x /bin/sudo || -x /usr/bin/sudo ]]; then
        echo "sudo $*"
        sudo -H $@
    else
        echo "Glances requires root privileges to install."
        echo "Please run this script as root."
        exit 1
    fi
}

# Detect distribution name
if [[ `which lsb_release 2>/dev/null` ]]; then
    # lsb_release available
    distrib_name=`lsb_release -is`
elif [[ `which sw_vers 2>/dev/null` ]]; then
    # sw_vers available (for macOS)
    distrib_name=`sw_vers -productName`
else
    # try other method...
    lsb_files=`find /etc -type f -maxdepth 1 \( ! -wholename /etc/os-release ! -wholename /etc/lsb-release -wholename /etc/\*release -o -wholename /etc/\*version \) 2> /dev/null`
    for file in $lsb_files; do
        if [[ $file =~ /etc/(.*)[-_] ]]; then
            distrib_name=${BASH_REMATCH[1]}
            break
        else
            echo "Sorry, GlancesAutoInstall script is not compliant with your system."
            echo "Please read: https://github.com/nicolargo/glances#installation"
            exit 1
        fi
    done
fi

echo "Detected system:" $distrib_name

shopt -s nocasematch
# Let's do the installation
if [[ $distrib_name == "ubuntu" || $distrib_name == "LinuxMint" || $distrib_name == "debian" || $distrib_name == "Raspbian" || $distrib_name == "neon" || $distrib_name == "elementary" ]]; then
    # Ubuntu/Debian variants

    # Set non interactive mode
    set -eo pipefail
    export DEBIAN_FRONTEND=noninteractive

    # Make sure the package repository is up to date
    #do_with_root apt-get -y update

    # Install prerequirements
    do_with_root apt-get install -y python-pip python-dev python-docker gcc lm-sensors wireless-tools

else
    # Unsupported system
    echo "Sorry, GlancesAutoInstall script is not compliant with your system."
    echo "Please read: https://github.com/nicolargo/glances#installation"
    exit 1

fi

shopt -u nocasematch


# Glances issue #922: Do not install PySensors (SENSORS)
DEPS="setuptools glances[action,batinfo,browser,cpuinfo,docker,export,folders,gpu,graph,ip,raid,snmp,web,wifi]"

# Install libs
# do_with_root pip install --upgrade pip
do_with_root pip install --quiet $DEPS

# Install or upgrade Glances from the Pipy repository
if [[ -x /usr/local/bin/glances || -x /usr/bin/glances ]]; then
    # Upgrade libs
    do_with_root pip install --quiet --upgrade $DEPS
    do_with_root pip install --quiet --upgrade glances
else
    echo "Install Glances"
    # Install Glances
    do_with_root pip install --quiet glances
fi
