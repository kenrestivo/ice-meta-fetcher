### Building and running your application

When you're ready, run the script by executing:
`docker run ice-meta-fetcher`.

### Deploying your application

First, build your image, e.g.: `docker build -t ice-meta-fetcher:latest .`.
If your cloud uses a different CPU architecture than your development
machine (e.g., you are on a Mac M1 and your cloud provider is amd64),
you'll want to build the image for that platform, e.g.:
`docker build --platform=linux/amd64 -t ice-meta-fetcher:latest .`.

Optionally, push it to your registry, e.g. `docker push myregistry.com/myapp`.
If you are simply running the command locally, you don't need to do this.

Consult Docker's [getting started](https://docs.docker.com/go/get-started-sharing/)
docs for more detail on building and pushing.

### References
* [Docker's Python guide](https://docs.docker.com/language/python/)
