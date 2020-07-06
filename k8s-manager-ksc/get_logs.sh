#!/bin/bash
set -x

#kubectl -n kube-system logs $(kubectl get pods --all-namespaces --no-headers -o custom-columns=":metadata.name")

all_pods=$(kubectl get pods --all-namespaces --no-headers -o custom-columns=":metadata.name")

    for pod  in ${all_pods[@]} ; do
        echo "working on ${pod}"
        kubectl -n kube-system logs ${pod}

    done
