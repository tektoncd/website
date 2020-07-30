#!/bin/bash

waitForCompletion() {
  local -r delay='0.75'
  local spinstr='\|/-'
  local temp
  while true; do
    sudo grep -i "done" $1 &> /dev/null
    if [[ "$?" -ne 0 ]]; then
      temp="${spinstr#?}"
      printf " [%c]  " "${spinstr}"
      spinstr=${temp}${spinstr%"${temp}"}
      sleep "${delay}"
      printf "\b\b\b\b\b\b"
    else
      break
    fi
  done
  printf "    \b\b\b\b"
  echo ""
}

showProgress()
{
  echo -n "Starting cluster"
  waitForCompletion /opt/.clusterstarted
  echo -n "Installing Tekton Pipelines"
  waitForCompletion /opt/.pipelinesinstalled
  echo -n "Installing Tekton Dashboard"
  waitForCompletion /opt/.dashboardinstalled
  echo -n "Installing Tekton CLI"
  waitForCompletion /opt/.tkninstalled
  echo -n "Waiting for pods to be ready"
  waitForCompletion /opt/.podsready
  echo -n "Configuring ingress"
  waitForCompletion /opt/.ingressconfigured
  # echo -n "Completing"
  # waitForCompletion /opt/.backgroundfinished
  echo "Ready"
  echo ""
}

showProgress
