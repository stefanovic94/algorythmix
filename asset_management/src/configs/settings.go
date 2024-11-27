package configs

import (
	"asset_management/src/libs/logging"
	"github.com/caarlos0/env/v11"
)

// Settings struct holds references to all env variables and settings
type SettingsType struct {
	Environment             string `env:"ENVIRONMENT" envDefault:"dev"`
	MongodbConnectionString string `env:"MONGODB_CONNECTION_STRING,required" envDefault:"mongodb://localhost:27017/"`
}

func GetSettings() SettingsType {
	log := logger.GetLogger()

	// parse
	var cfg SettingsType
	err := env.Parse(&cfg)

	if err != nil {
		log.Warn().Err(err).Msg("Error parsing env variables")
	}

	return cfg
}

var Settings = GetSettings()
