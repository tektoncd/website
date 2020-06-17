The example Python app provided with the scenario is actually a client
utility that connects to a remote service and retrieves information. For
security reasons, before talking with the server it must use a credential
to authenticate itself. 

One may put the credential in the tests, however, it is obviously not very
secure; in reality, most organizations mount credentials (as environment
variables, or files) during the test so that only those who have full
access to the test infrastructure may see them. Tekton uses the standard
Kubernetes volumes to support this use case, allowing developers to share
files and directories between environments.

In this section, you will use this feature to mount a
[Kubernetes Secret](https://kubernetes.io/docs/concepts/configuration/secret/)
in the Tekton task so that the client app may use it to connect to the server.

First, create a secret. An example is available at
`website/tutorials/katacoda/tasks/src/tekton-katacoda/secrets/secret.yaml`:

```yaml
apiVersion: v1
kind: Secret
metadata:
    # The name of the secret
    name: example-secret
type: Opaque
data:
    # The actual secret in the form of a key-value pair
    apiKey: example-api-key
```

To apply this secret, run the command below:

`kubectl apply -f website/tutorials/katacoda/tasks/src/tekton-katacoda/secrets/secret.yaml`{{execute}}

With the secret ready, you can now edit the Tekton task to use it during
the tests. Open `website/tutorials/katacoda/tasks/src/tekton-katacoda/tasks/taskTemplate.yaml`
and make the modifications below:

```yaml
specs:
  steps:
  - name: ...
    image: ...
		script: |
		  #!/bin/bash
			...
    # Mount the secret volume at path /etc/credential
    volumeMounts:
    - name: credential
      mountPath: /etc/credential
  # Ask the task to use the secret created earlier as a volume
  volumes:
  - name: credential
    secret:
      secretName: example-secret
  ...
```

With this setup, Tekton will automatically create a file with the name `apiKey`
in the path `/etc/credential`. The file includes the value of the secret
key-value pair, `example-api-key`. The tests have been configured to read 
the file at the specified path and load a credential from it.

## More about volumes

You can mount many different types of volumes other than secrets.
Common use cases include:

* [`emptyDir` volumes](https://kubernetes.io/docs/concepts/storage/volumes/#emptydir)
for sharing data across steps in a task or different tasks.
* [`configMap` volumes](https://kubernetes.io/docs/concepts/storage/volumes/#configmap)
for sharing a configuration across steps in a task or different tasks.
* A local file or directory, such as a socket

[You can learn more about Kubernetes volumes here](https://kubernetes.io/docs/concepts/storage/volumes/).
