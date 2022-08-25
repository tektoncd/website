<!--
---
title: "Install the Tekton CLI"
linkTitle: "Tekton CLI"
weight: 4
description: >
  Install `tkn`, the Tekton CLI
---
-->

The Tekton CLI, `tkn`, provides easy interaction with the Tekton components. The
CLI is available on all major platforms. You can also build it from source or
set it up as a kubectl plugin.

## Prerequisites

To install `tkn` using a package manager:

- MacOS: [Homebrew].

- Windows:  [Chocolatey].

- Linux: APT or DNF for deb-based or rpm-based distributions, respectively.  

[homebrew]: https://brew.sh/
[chocolatey]: https://chocolatey.org/ 

## Installation

{{% tabs %}}

{{% tab "macOS" %}}

- **[Homebrew][homebrew-formula] installation**

  ```bash
  brew install tektoncd-cli
  ```

- **Manual installation**

  Download the tarball from the [releases page][tkn-release]. After
  downloading the file, extract it to a directory in your `PATH`. For example,
  to install the version `0.23.1` for a `x86-64` mac:

  ```bash
  curl -LO https://github.com/tektoncd/cli/releases/download/v0.23.1/tkn_0.23.1_Darwin_x86_64.tar.gz
  sudo tar -xvzf tkn_0.23.1_Darwin_x86_64.tar.gz -C /usr/local/bin/ tkn
  ```

[homebrew-formula]: https://formulae.brew.sh/formula/tektoncd-cli
[tkn-release]: https://github.com/tektoncd/cli/releases

{{% /tab %}}

{{% tab "Windows" %}}

- **Chocolatey installation**

  ```cmd
  choco install tektoncd-cli --confirm
  ```

- **Manual installation**

  Download the `.zip` file from the [`tkn` Releases page][tkn-release].
  After downloading the file, add it to your `Path`:

  1.  Uncompress the `.zip` file.
  1.  Open **Control Panel** > **System and Security** > **System** > **Advanced System Settings**.
  1.  Click **Environment Variables**, select the `Path` variable and click **Edit**.
  1.  Click **New** and add the path to your uncompressed file.
  1.  Click **OK**.

[tkn-release]: https://github.com/tektoncd/cli/releases

{{% /tab %}}

{{% tab "Linux" %}}

-   **Debian, Ubuntu, and other deb-based distros**

    - Using the system package manager:
   
      ```bash
      sudo apt update;sudo apt install -y gnupg
      sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 3EFE0E0A2F2F60AA
      echo "deb http://ppa.launchpad.net/tektoncd/cli/ubuntu eoan main"|sudo tee /etc/apt/sources.list.d/tektoncd-ubuntu-cli.list
      sudo apt update && sudo apt install -y tektoncd-cli
      ```

    - Manual installation:

      You can use `curl` to download and install a particular version from
      [releases page][tkn-release]. For example, the version `0.23.1` for
      `x86-64`:

      ```bash
      curl -LO https://github.com/tektoncd/cli/releases/download/v0.23.1/tektoncd-cli-0.23.1_Linux-64bit.deb
      sudo dpkg -i tektoncd-cli-0.23.1_Linux-64bit.deb
      ```

-   **Fedora, CentOS, and other rpm-based distros**

    - Using the system package manager, there's an unofficial repository you can use:

      ```bash
      dnf copr enable chmouel/tektoncd-cli
      dnf install tektoncd-cli
      ```

    - Manual installation:

      You can use `curl` to download and install a particular version from
      [releases page][tkn-release]. For example, the version `0.23.1` for
      `x86-64`:

      ```bash
      curl -OL https://github.com/tektoncd/cli/releases/download/v0.23.1/tektoncd-cli-0.23.1_Linux-64bit.rpm
      rpm -Uvh tektoncd-cli-0.23.1_Linux-64bit.rpm
      ```

-   **Other Linux distributions**

    Find the tarball of the Tekton CLI release for the platform (`ARM` or
    `X86-64`) you would like to install on the [releases page][tkn-release] and copy
    the binary to a folder in your `PATH`. For example, to install version `0.23.1`
    for `x86-64` in `/usr/local/bin`:

    ```bash
    curl -LO https://github.com/tektoncd/cli/releases/download/v0.23.1/tkn_0.23.1_Linux_arm64.tar.gz
    sudo tar -xvzf tkn_0.23.1_Linux_arm64.tar.gz -C /usr/local/bin/ tkn
    ```

[tkn-release]: https://github.com/tektoncd/cli/releases

{{% /tab %}}

{{% /tabs %}}

### Build the binary from source

To build `tkn` from the source, set up your [Go](https://golang.org/)
development environment, clone the [GitHub repository for
`tkn`](https://github.com/tektoncd/cli), and run the following commands in the
cloned directory:

```bash
export GO111MODULE=on
make bin/tkn
```

The `tkn` executable will be available at `/bin`.

### Add as a `kubectl` plugin

After you install `tkn`, to add it as a [`kubectl` plugin][kplugin] run the
following command:

```bash
ln -s /usr/local/bin/tkn /usr/local/bin/kubectl-tkn
```

{{% alert title="Note" color="info" %}}
*The previous command assumes that your `tkn` executable is available at
`/usr/local/bin/tkn`. Adjust the path if your executable is at a different
location.*
{{% /alert %}}

To verify that the plugin was successfully added:

```bash
kubectl plugin list
```

The output lists `kubectl-tkn` as one of the plugins.

## Further reading

See all supported commands and options in the [Tekton CLI reference documentation][tkn-ref]. 

[kplugin]: https://kubernetes.io/docs/tasks/extend-kubectl/kubectl-plugins/#using-a-plugin
[tkn-ref]: https://github.com/tektoncd/cli/tree/main/docs/cmd
