echo "# See Tekton in action!" | pv -qL 12
echo "# Tekton is available as Kubernetes Custom Resource Definitions " | pv -qL 12
echo "# (CRD) that you can install in your Kubernetes cluster" | pv -qL 12
echo '# And it uses container images to perform operations in your ' | pv -qL 12
echo '# CI/CD pipeline' | pv -qL 12
echo "# Let's say you would like to compile a Go program with Tekton" | pv -qL 12
echo '# First, write a Tekton task:' | pv -qL 12
echo 'cat task.yaml' | pv -qL 12
cat task.yaml | lolcat
echo ''
echo '------------------------' | pv -qL 6
echo '# And apply it to your Kubernetes cluster:' | pv -qL 12
echo 'kubectl apply -f task.yaml' | pv -qL 12
echo '# Next, organize your task into a Tekton pipeline:' | pv -qL 12
echo 'cat pipeline.yaml' | pv -qL 12
cat pipeline.yaml | lolcat
echo ''
echo '------------------------' | pv -qL 6
echo '# And apply it to your Kubernetes cluster as well:' | pv -qL 12
echo 'kubectl apply -f pipeline.yaml' | pv -qL 12
echo '# And it is done :)' | pv -qL 12
echo '# You can run your pipeline manually, or trigger it every time an ' | pv -qL 12
echo '# event arrives, such as one from a GitHub webhook' | pv -qL 12
echo '# Tekton has a dashboard and a CLI as well' | pv -qL 12
echo '# Learn more about Tekton at ' | pv -qL 12
echo '# tekton.dev/docs' | cat | pv -qL 12 | lolcat
echo '# or play with one of our interactive tutorials at ' | pv -qL 12
echo '# tekton.dev/try' | cat | pv -qL 12 | lolcat
