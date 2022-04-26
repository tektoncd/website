<!--
---
title: "Install Tekton Dashboard"
linkTitle: "Tekton Dashboard"
weight: 4
description: >
  Install Tekton Dashboard on you cluster
---
-->

## Prerequisites

-   [Kubernetes] cluster version 1.18.0 or later.
-   Admin privileges to the user running the installation.
-   [Kubectl].
-   [Tekton Pipelines](/docs/installation/pipelines/).
-   [Tekton Triggers](/docs/installation/triggers/) (Optional).

## Installation

Every Tekton Dashboard version supports specific Tekton Pipelines and Tekton
Triggers versions. Check [the compatibility table][compat-table] to find out
which version of Tekton Dashboard works for your cluster.

{{% tabs %}}

{{% tab "Kubernetes" %}}

1.  Depending on which version of Tekton Pipelines you want to install, run one
    of the following commands:

    -   **Latest official release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml
        ```

    -   **Specific Release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/dashboard/previous/VERSION_NUMBER/tekton-dashboard-release.yaml
        ```

        Replace `VERSION_NUMBER` with the numbered version you want to install.
        For example, `v0.12.0`.

    -   **Nightly release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases-nightly/dashboard/latest/tekton-dashboard-release.yaml
        ```

1.  To monitor the installation, run:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When all components show `Running` under the `STATUS` column the installation is
    complete. Hit *Ctrl + C* to stop monitoring.

{{% /tab %}}

{{% tab "OpenShift" %}}

1.  Depending on which version of Tekton Pipelines you want to install, run one
    of the following commands:

    -   **Latest official release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/dashboard/latest/openshift-tekton-dashboard-release.yaml \
        --validate=false
        ```

    -   **Specific Release**

        ```bash
        kubectl apply --filename \
        https://storage.googleapis.com/tekton-releases/dashboard/previous/VERSION_NUMBER/openshift-tekton-dashboard-release.yaml \
        --validate=false
        ```

        Replace `VERSION_NUMBER` with the numbered version you want to install.
        For example, `v0.12.0`.

1.  To monitor the installation, run:

    ```bash
    kubectl get pods --namespace tekton-pipelines --watch
    ```

    When all components show `Running` under the `STATUS` column the installation is
    complete.

{{% alert title="Note" color="info" %}}
If you installed Tekton Pipelines and Triggers without using the OpenShift
Pipelines operator, change the following args:

- `--pipelines-namespace=openshift-pipelines`
- `--triggers-namespace=openshift-pipelines`

Set their values to the namespace where Pipelines and Triggers were respectively
deployed.
{{% /alert %}}

{{% /tab %}}

{{% /tabs %}}

### Using the installer script

Releases `v0.8.0` and later provide an installer script to simplify deploying
Tekton Dashboard with custom options.

For example, to install the latest release in read-only mode:

```bash
curl -sL https://raw.githubusercontent.com/tektoncd/dashboard/main/scripts/release-installer | \
   bash -s -- install latest --read-only
```

See the developer documentation on [how to use the installer][installer-script]
for more information.

## Accessing the Dashboard

By default, the Dashboard is not exposed outside the cluster.

There are several solutions to access the Dashboard UI depending on your setup.

### Using kubectl proxy

The Dashboard can be accessed through its ClusterIP Service by running `kubectl
proxy`.

Assuming `tekton-pipelines` is the install namespace for the Dashboard, run the
following command:

```bash
kubectl proxy
```

Browse
http://localhost:8001/api/v1/namespaces/tekton-pipelines/services/tekton-dashboard:http/proxy/
to access your Dashboard.

### Using kubectl port-forward

An alternative way to access the Dashboard is using `kubectl port-forward`.

Assuming `tekton-pipelines` is the install namespace for the Dashboard, run the following command:

```bash
kubectl --namespace tekton-pipelines port-forward svc/tekton-dashboard 9097:9097
```

Browse http://localhost:9097 to access your Dashboard.

### Using an Ingress rule

A more advanced solution is to expose the Dashboard through an `Ingress` rule.
This way the Dashboard can be accessed as a regular website without requiring
`kubectl`.

Assuming you have an [ingress controller][ingress-controller] up and running in
your cluster, and that `tekton-pipelines` is the namespace where the Dashboard
is installed, run the following command to create the `Ingress` resource:

```bash
# replace DASHBOARD_URL with the hostname you want for your dashboard
# the hostname should be setup to point to your ingress controller
DASHBOARD_URL=dashboard.domain.tld
kubectl apply -n tekton-pipelines -f - <<EOF
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tekton-dashboard
  namespace: tekton-pipelines
spec:
  rules:
  - host: $DASHBOARD_URL
    http:
      paths:
      - pathType: ImplementationSpecific
        backend:
          service:
            name: tekton-dashboard
            port:
              number: 9097
EOF
```

You can now access the Dashboard UI at `http(s)://dashboard.domain.tld` in your
browser (assuming the host configured in the ingress is `dashboard.domain.tld`)

There are some additional considerations to keep in mind in this case:

- The exact `Ingress` resource definition may vary depending on the ingress
  controller installed in the cluster. Some specific annotations may be required
  for the ingress controller to process the `Ingress` resource correctly.

- If you don't have access to a domain you can use the freely available
  [`nip.io`](https://nip.io/) service.

The following example uses the NGINX ingress controller to expose the Dashboard
on a specific path instead of at the root of the domain:

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: tekton-dashboard
  namespace: tekton-pipelines
  annotations:
    kubernetes.io/ingress.class: nginx
    nginx.ingress.kubernetes.io/rewrite-target: /$2
spec:
  rules:
  - host: domain.tld
    http:
      paths:
      - path: /tekton(/|$)(.*)
        backend:
          service:
            name: tekton-dashboard
            port:
              number: 9097
```

You can then access the Dashboard UI at `http(s)://domain.tld/tekton/`.

### Access control

The Dashboard does not provide its own authentication or authorization, however
it will pass on any authentication headers provided to it by a proxy deployed in
front of the Dashboard. These are then handled by the Kubernetes API server
allowing for full access control via [Kubernetes RBAC][k-rbac]. In case of
forbidden access the Dashboard will display corresponding error notifications.

See the walk-throughs for an example of [enabling authentication using
oauth2-proxy][oauth2-wt].

By default the Dashboard accesses resources and performs actions in the cluster
using the permissions granted to its own ServiceAccount (the `tekton-dashboard`
ServiceAccount in the `tekton-pipelines` namespace). If you wish to have the
Dashboard perform actions on behalf of the authenticated user or some other
ServiceAccount this can be achieved via [user impersonation][user-auth].  This
is known to work with a number of popular solutions including oauth2-proxy,
Keycloak, OpenUnison, Traefik, Istio's EnvoyFilter, and more.

Typically, when configuring impersonation you would have the proxy forward its
ServiceAccount token in the `Authorization` header, and details of the user and
groups in the `Impersonate-User` and `Impersonate-Group` headers respectively.
See the docs of your chosen solution for details.

When using a reverse proxy, with impersonation headers or the user's account,
you should remove the Dashboard's privileges to better maintain a "least
privileged" approach.  This will make it less likely that the Dashboard's
`ServiceAccount` will be abused:


```
kubectl delete clusterrolebinding -l rbac.dashboard.tekton.dev/subject=tekton-dashboard
kubectl delete rolebinding -l rbac.dashboard.tekton.dev/subject=tekton-dashboard -n tekton-pipelines
```

If you're using one of these proxies to provide authentication but still want to
use the Dashboard's ServiceAccount to access the Kubernetes APIs you may need to
modify the proxy config to prevent it from sending the `Authorization` header on
upstream requests to the Dashboard. Some examples of relevant config:

- [oauth2-proxy]: add the `--pass-authorization-header=false` command line
  argument or its equivalent to your config.

- [Istio EnvoyFilter][istio-filter]: the external authentication service should
  return a custom header `x-envoy-auth-headers-to-remove: Authorization`.

- [Traefik]: `removeHeader: true`

## Uninstalling the Dashboard on Kubernetes

The Dashboard can be uninstalled by running the following command:

```bash
kubectl delete --filename \
https://storage.googleapis.com/tekton-releases/dashboard/latest/tekton-dashboard-release.yaml
```

Use the URL corresponding to your installation.

## Further reading

To get started with Tekton Dashboard, see the [tutorial].

To add more functionality to your Tekton Dashboard, see the [Tekton Dashboard
extensions][dashboard-extensions].

[kubernetes]: https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/
[kubectl]: https://kubernetes.io/docs/tasks/tools/#kubectl
[compat-table]: https://github.com/tektoncd/dashboard/blob/main/README.md#which-version-should-i-use
[installer-script]: https://github.com/tektoncd/dashboard/blob/main/docs/dev/installer.md
[ingress-controller]: https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/
[k-rbac]:https://kubernetes.io/docs/reference/access-authn-authz/rbac/
[oauth2-wt]: https://github.com/tektoncd/dashboard/tree/main/docs/walkthrough
[user-auth]:https://kubernetes.io/docs/reference/access-authn-authz/authentication/#user-impersonation
[oauth2-proxy]: https://oauth2-proxy.github.io/oauth2-proxy/docs/configuration/overview#command-line-options
[istio-filter]: https://www.envoyproxy.io/docs/envoy/latest/api-v3/service/auth/v3/external_auth.proto
[traefik]: https://doc.traefik.io/traefik/v2.0/middlewares/basicauth/#removeheader
[tutorial]: https://github.com/tektoncd/dashboard/tree/main/docs/tutorial
[dashboard-extensions]: https://github.com/tektoncd/dashboard/blob/main/docs/extensions.md 
