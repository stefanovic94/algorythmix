package assets

import (
	"github.com/google/uuid"

	Entities "asset_management/src/domain/entities"
	DomainEvents "asset_management/src/domain/events"
	AssetRepository "asset_management/src/infrastructure/adapters"
	"asset_management/src/libs/logging"
)

func CreateAssetCommand(c chan<- Entities.Asset, symbol string) {
	log := logger.GetLogger()

	log.Info().Msg("creating new asset...")

	id := uuid.NewString()

	// TODO get asset by its symbol from external API and populate entity model

	obj := Entities.Asset{
		ID:     id,
		Symbol: symbol,
	}

	go AssetRepository.CreateAsset(obj)

	go DomainEvents.AssetCreated(c, obj)

	log.Info().Str("id", id).Msg("asset created...")
}
