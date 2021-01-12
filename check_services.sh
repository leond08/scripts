#!/usr/bin/env bash
# shellcheck disable=SC1090

set -e

is_command() {
    # Checks for existence of string passed in as only function argument.
    # Exit value of 0 when exists, 1 if not exists. Value is the result
    # of the `command` shell built-in call.
    local check_command="$1"

    command -v "${check_command}" >/dev/null 2>&1
}

check_service_active() {
    # If systemctl exists,
    if is_command systemctl ; then
      # use that to check the status of the service
      systemctl is-active "${1}" &> /dev/null
    # Otherwise,
    else
      # fall back to service command
      service "${1}" status &> /dev/null
    fi
}

# Start/Restart service passed in as argument
restart_service() {
  # Local, named variables
  # If systemctl exists,
  if is_command systemctl ; then
    # use that to restart the service
    systemctl restart "${1}" &> /dev/null
  # Otherwise,
  else
    # fall back to the service command
    service "${1}" restart &> /dev/null
  fi
}

if check_service_active "S70pikonekcaptive" ; then
  PIKONEKCAPTIVE_ACTIVE=true
else
  PIKONEKCAPTIVE_ACTIVE=false
fi

if check_service_active "S70pikonekcaptivefw" ; then
  PIKONEKCAPTIVEFW_ACTIVE=true
else
  PIKONEKCAPTIVEFW_ACTIVE=false
fi

if [[ "${PIKONEKCAPTIVE_ACTIVE}" == false ]]; then
  restart_service S70pikonekcaptive
fi

if [[ "${PIKONEKCAPTIVEFW_ACTIVE}" == false ]]; then
  restart_service S70pikonekcaptivefw
fi