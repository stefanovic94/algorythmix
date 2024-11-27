package logger

import (
	"os"

	"github.com/rs/zerolog"
)

func initLogger() zerolog.Logger {
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
	// Create a new logging instance and configure it
	logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
	return logger
}

var logger = initLogger()

func GetLogger() zerolog.Logger {
	return logger
}
