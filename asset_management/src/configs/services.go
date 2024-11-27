package configs

import (
	"asset_management/src/libs/logging"
	"context"
	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

// Services struct holds references to external tools
type ServicesType struct {
	Mongodb *mongo.Client
}

// Connect Method to initialize and connect to all services (if needed)
func Connect(ctx context.Context, settings SettingsType) (*mongo.Client, error) {
	mdbClient, err := mongo.Connect(ctx, options.Client().ApplyURI(settings.MongodbConnectionString))
	if err != nil {
		return nil, err
	}
	return mdbClient, nil
}

// InitializeServices initializes and returns a Services struct with all necessary services
func InitializeServices(ctx context.Context) *ServicesType {
	log := logger.GetLogger()

	log.Info().Msg("Initializing services...")

	mdbClient, err := Connect(ctx, Settings)
	if err != nil {
		log.Fatal().Err(err).Msg("Error connecting to MongoDB")
	}

	log.Print(mdbClient.Ping(ctx, nil))

	return &ServicesType{
		Mongodb: mdbClient,
	}
}

var Services *ServicesType
