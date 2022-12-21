FROM registry.efarda.ir/python:3.9.6-alpine

RUN apk update
RUN apk upgrade
# RUN apk search curl
RUN apk --no-cache add curl


ENTRYPOINT ["tail"]
CMD ["-f","/dev/null"]