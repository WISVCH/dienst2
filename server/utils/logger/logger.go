package logger

import (
	log "github.com/sirupsen/logrus"
)

/*
 * A small note on this package:
 * This package is meant as a simple wrapper to avoid importing the logrus
 * library in the code directly, and also to log errors and such to Sentry
 * without needing a separate call in the production code. Note that for
 * specific logging, like incoming requests, the logrus package is used directly
 */

type LogFields map[string]interface{}

func Error(location string, fields LogFields, err error) {
	fields["location"] = location
	logWithFields := log.WithFields(log.Fields(fields))
	logWithFields.Error(err.Error())
}

func Warn(location string, fields LogFields, err error) {
	fields["location"] = location
	logWithFields := log.WithFields(log.Fields(fields))
	logWithFields.Warn(err.Error())
}

func Info(location string, fields LogFields, message string) {
	fields["location"] = location
	logWithFields := log.WithFields(log.Fields(fields))
	logWithFields.Info(message)
}

func Debug(location string, fields LogFields, message string) {
	fields["location"] = location
	logWithFields := log.WithFields(log.Fields(fields))
	logWithFields.Debug(message)
}
