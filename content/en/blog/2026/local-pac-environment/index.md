---
title: "Setting Up a Local Pipelines-as-Code Development Environment"
linkTitle: "Setting Up a Local Pipelines-as-Code Development Environment"
date: 2026-03-28
author: "Akshay Pant, RedHat"
description: >
  Learn how to create a complete local Pipelines-as-Code environment for safe experimentation and development using startpaac.
---

The [startpaac](https://github.com/pipelines-as-code/startpaac) tool creates a complete local Pipelines-as-Code environment by building and deploying PAC directly from your source code, giving you a safe sandbox for experimentation and development before touching production.

## Benefits of Local Development

A local PAC environment provides several key advantages:

- **Safe experimentation**: Test configurations and features without affecting production systems
- **Complete visibility**: Observe how PAC components interact in real-time
- **Full control**: Pause, inspect, and debug any scenario at your own pace
- **Real PAC system**: Build and run PAC from source against real GitHub repositories — not a simulator

## Prerequisites

### System Requirements

- **CPU**: Minimum 4 cores (8 recommended for optimal performance)
- **Memory**: 8GB RAM minimum (16GB recommended)
- **Storage**: 20GB free disk space minimum (50GB recommended)

### Required Tools

Install these tools before running startpaac:

```bash
# Core container and Kubernetes tools
docker >= 20.10
kind >= 0.20.0
helm >= 3.10
kubectl >= 1.27

# Go and container build tools
ko >= 0.14

# CLI utilities
gum >= 0.11
jq >= 1.6
minica

# Tekton CLI
tkn >= 0.32.0
```

### Platform-Specific Requirements

**macOS/BSD Users:**
```bash
brew install coreutils gnu-sed
```

**Optional Tools:**
- `pass`: Password manager for enhanced secret security

## Understanding startpaac

[startpaac](https://github.com/pipelines-as-code/startpaac) is a comprehensive development tool that creates a complete PAC ecosystem on your local machine by building and deploying Pipelines-as-Code directly from your local source code.

**Important**: Unlike production installations that use pre-built releases, startpaac is specifically designed for PAC development and contribution workflows. It requires:
- A local checkout of the [Pipelines-as-Code source repository](https://github.com/tektoncd/pipelines-as-code)
- Configuration of the `PAC_DIR` variable to point to your local PAC source code
- The `ko` build tool to compile and deploy your local PAC code to the Kind cluster
- This allows you to test code changes, contributions, or custom builds immediately

### What startpaac Installs

**Core Components (Always Included):**
- Kind Kubernetes cluster with local registry
- Tekton Pipelines
- Nginx ingress controller

**Recommended for Learning:**
- Pipelines-as-Code controller and webhook
- Tekton Dashboard for visual pipeline monitoring
- Forgejo for testing complete Git workflows

**Optional Extensions:**
- Tekton Triggers for advanced event handling
- Tekton Chains for supply chain security
- PostgreSQL database
- GitHub Second Controller for enterprise setups

## Installation and Setup

### Getting startpaac

First, clone the startpaac repository:

```bash
git clone https://github.com/pipelines-as-code/startpaac
cd startpaac
```

startpaac needs to know where your PAC source code is located. Create a configuration file to specify this:

```bash
mkdir -p ~/.config/startpaac
cat <<EOF > ~/.config/startpaac/config
TARGET_HOST=local
PAC_DIR=/path/to/your/pipelines-as-code
PAC_SECRET_FOLDER=~/secrets
EOF
```

Replace `/path/to/your/pipelines-as-code` with the actual path to your PAC source directory. If you don't have the PAC source code yet, clone it:

```bash
git clone https://github.com/tektoncd/pipelines-as-code
# Then update PAC_DIR in the config to point to this directory
```

This setup allows startpaac to build your local PAC source code and deploy it to the Kind cluster.

### Interactive Installation

Launch the interactive setup:

```bash
./startpaac
```

The tool presents a checkbox menu for selecting components. For learning PAC fundamentals, select:

- ✅ **Pipelines-as-Code** (core functionality)
- ✅ **Tekton Dashboard** (pipeline monitoring and logs)
- ✅ **Forgejo** (complete Git workflow testing)
- ⬜ **Tekton Triggers** (optional: advanced event triggers)
- ⬜ **Tekton Chains** (optional: supply chain security)
- ⬜ **PostgreSQL, GitHub Second Controller** (optional: enterprise features)

startpaac remembers your configuration for future runs, streamlining subsequent setups.

### Installation Process

The installation typically takes 5-10 minutes depending on your internet connection. Monitor progress and verify successful deployment:

```bash
# Verify PAC components
kubectl get pods -n pipelines-as-code

# Check Tekton Pipeline installation
kubectl get pods -n tekton-pipelines

# Verify Kind cluster status
kind get clusters
```

All pods should show `Running` status before proceeding.

### Working with PAC Source Code

Since startpaac builds from your local PAC source, you can make changes and redeploy them immediately:

```bash
# Make changes to PAC source code
cd /path/to/your/pipelines-as-code
# Edit files, make improvements, etc.

# Redeploy your changes to the Kind cluster
cd /path/to/startpaac
./startpaac -p  # Redeploy PAC with your changes

# Or redeploy just the controller component
./startpaac -c controller
```

This development workflow allows you to:
- Test local PAC modifications immediately
- Debug PAC components with your own builds  
- Contribute features back to the PAC project
- Experiment with unreleased PAC functionality

## GitHub Integration Setup

PAC requires webhook connectivity from GitHub to your local cluster. Since local clusters aren't internet-accessible, startpaac automatically deploys [gosmee](https://github.com/chmouel/gosmee) to handle webhook forwarding.

### GitHub Application Configuration

#### 1. Create GitHub Application

Navigate to [GitHub Apps creation page](https://github.com/settings/apps/new) and fill in the required fields:

- **GitHub App name**: Choose a unique name (e.g., "My PAC Development App")
- **Homepage URL**: Can be your GitHub profile or any placeholder URL
- **Webhook URL**: Use `https://hook.pipelinesascode.com/YOUR_UNIQUE_ID` (get this from gosmee setup)
- **Webhook secret**: Generate a random secret string

#### 2. Configure GitHub App Permissions

Set the following **Repository permissions**:
- **Contents**: Read (to access repository files)
- **Issues**: Write (for status updates)
- **Metadata**: Read (repository metadata)
- **Pull requests**: Write (for status checks and comments)
- **Checks**: Write (for check runs)

Set the following **Events** to subscribe to:
- Pull request
- Push
- Issue comment

#### 3. Install the GitHub App

After creating the app:
1. Note down the **App ID** from the app settings page
2. Generate a **private key** and download it
3. Install the app on your test repository

#### 4. Set Up Webhook Forwarding

Since your local cluster isn't accessible from the internet, you need webhook forwarding. startpaac automatically sets up gosmee, but you need the webhook URL:

1. When you run startpaac, look for a line in the output like `Gosmee URL: https://hook.pipelinesascode.com/ABC123`
2. Use this URL as your GitHub App webhook URL
3. Set a webhook secret (any random string)

#### 5. Create Secret Files

Create the secret files that startpaac expects:

```bash
mkdir -p ~/secrets

# GitHub App ID (numeric ID from the app settings page)
echo "123456" > ~/secrets/github-application-id

# GitHub App private key (content of the .pem file you downloaded)
cat > ~/secrets/github-private-key <<'EOF'
-----BEGIN RSA PRIVATE KEY-----
[Your private key content here]
-----END RSA PRIVATE KEY-----
EOF

# Webhook URL from gosmee (you'll get this when running startpaac)
echo "https://hook.pipelinesascode.com/YOUR_UNIQUE_ID" > ~/secrets/smee

# Webhook secret (same random string you set in GitHub App)
echo "your-webhook-secret-here" > ~/secrets/webhook.secret
```

#### 6. Verify Configuration

After setting up the secrets, verify they're configured correctly:

```bash
ls -la ~/secrets/
# Should show: github-application-id, github-private-key, smee, webhook.secret
```

## Creating a Test Repository

Use the official PAC demo repository as your testing ground:

1. **Generate from Template**
   Visit [PAC demo repository](https://github.com/pipelines-as-code/pac-demo/generate) and create a new repository (e.g., `pac-playground`)

2. **Install GitHub Application**
   Install your GitHub App on the newly created repository

3. **Clone Locally**
   ```bash
   git clone https://github.com/yourusername/pac-playground
   cd pac-playground
   ```

## PAC Repository Configuration

Configure PAC to monitor your repository using the Tekton CLI:

```bash
tkn pac create repository
```

This intelligent command:
- Auto-detects your repository URL from Git metadata
- Creates a dedicated namespace for pipeline execution
- Analyzes your codebase and generates appropriate pipeline templates
- Sets up the Repository Custom Resource (CR) in your cluster

The demo repository contains a Go project, so it automatically creates a pipeline with golangci-lint integration.

### Examining Generated Configuration

Review the generated pipeline configuration:

```bash
cat .tekton/pipelinerun.yaml
```

The file includes comprehensive comments explaining each component and how PAC processes the pipeline definition.

## Testing Your First Pipeline

Execute your first PAC pipeline run to verify the complete integration:

```bash
# Create a feature branch
git checkout -b test-pac-pipeline

# Add generated configuration
git add .tekton/

# Commit changes
git commit -m "Add PAC pipeline configuration"

# Push to GitHub
git push origin test-pac-pipeline
```

### Creating a Pull Request

Create a pull request from your branch on GitHub. This triggers the PAC workflow:

1. GitHub sends webhook to gosmee endpoint
2. gosmee forwards webhook to local PAC installation  
3. PAC detects `.tekton/` directory and initializes pipeline
4. Kubernetes cluster executes the pipeline
5. Results are posted back to GitHub as status checks

### Monitoring Pipeline Execution

Track pipeline progress using multiple methods:

**CLI Monitoring:**
```bash
# List pipeline runs
tkn pipelinerun list -n pac-playground-pipelines

# Follow logs in real-time
tkn pipelinerun logs --last -f -n pac-playground-pipelines
```

**Dashboard Access:**

startpaac automatically sets up ingress for the Tekton Dashboard. Access it directly at:

`https://dashboard.127.0.0.1.nip.io`

## Learning from Intentional Failures

The demo repository includes deliberate linting errors that serve as learning opportunities. When your first pipeline run encounters these issues, PAC demonstrates its error handling and feedback capabilities:

- Clear error reporting with specific line references
- Links between failures and source code locations  
- Actionable feedback for quick resolution

This shows PAC's strength in providing meaningful feedback rather than generic failure messages.

## Troubleshooting Common Issues

### Pipeline Not Triggering

**Check webhook forwarding:**
```bash
kubectl logs -n gosmee -l app.kubernetes.io/name=gosmee -f
```

### Resource Constraints

**Monitor cluster resource usage:**
```bash
kubectl top nodes
kubectl describe nodes
```

### Configuration Problems  

**Verify repository setup:**
```bash
tkn pac repository list
tkn pac repository describe <repository-name>
```

## Next Steps and Advanced Usage

With your local environment operational, explore PAC's advanced capabilities:

- **Code Development**: Modify PAC source code and see changes deployed immediately
- **Pipeline Annotations**: Experiment with different trigger conditions
- **Multi-Pipeline Scenarios**: Test complex workflow orchestration
- **GitHub Integration Patterns**: Understand various authentication methods
- **Custom Task Integration**: Incorporate specialized Tekton tasks
- **Feature Development**: Build and test new PAC features before contributing upstream

Check out the [startpaac documentation](https://github.com/pipelines-as-code/startpaac) and [Pipelines-as-Code guides](https://pipelinesascode.com/) to go deeper.
