# AWS-SAM-Layer-builder
AWS SAM (Lambda) layer builder with configuration for OpenAI

The layer is pre-configured to build latest python 3.12 and the zipped layer will be located in layers folder:
```bash
./build
```

To call from curl use this command providing local mp3 file name (@local_audio_file.mpe) and AWS Lambda url
```bash
$ curl -v -X POST -F audio='@local_audio_file.mp3' https://some_url.lambda-url.aws_region.on.aws
```
