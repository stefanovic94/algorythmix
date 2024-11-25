package configs

import (
	"os"

	"github.com/rs/zerolog"
)

func Logger() zerolog.Logger {
	zerolog.TimeFieldFormat = zerolog.TimeFormatUnix
	// Create a new logger instance and configure it
	logger := zerolog.New(os.Stdout).With().Timestamp().Logger()
	return logger
}
