package assets

import (
	"github.com/google/uuid"

	"asset_management/src/domain/entities"
	"asset_management/src/domain/events"
	"asset_management/src/libs/logging"
)

func CreateAssetCommand(c chan<- entities.Asset, symbol string) {
	log := logger.GetLogger()

	log.Info().Msg("creating new asset...")

	id := uuid.NewString()

	// TODO get asset by its symbol from external API and populate entity model

	obj := entities.Asset{
		ID:     id,
		Symbol: symbol,
	}

	go events.AssetCreated(c, obj)

	log.Info().Str("id", id).Msg("asset created...")
}
