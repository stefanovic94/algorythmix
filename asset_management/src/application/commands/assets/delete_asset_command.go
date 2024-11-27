package assets

import (
	DomainEvents "asset_management/src/domain/events"
	AssetRepository "asset_management/src/infrastructure/adapters"
	"asset_management/src/libs/logging"
)

func DeleteAssetCommand(c chan<- string, id string) {
	log := logger.GetLogger()

	log.Info().Str("id", id).Msg("deleting asset...")

	if err := AssetRepository.DeleteAsset(id); err != nil {
		log.Error().Err(err).Msg("error deleting asset")
		// TODO improve error handling
		panic(err)
	}

	go DomainEvents.AssetDeleted(c, id)

	log.Info().Str("id", id).Msg("asset deleted...")
}
