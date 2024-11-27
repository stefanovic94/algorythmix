package assets

import (
	DomainEvents "asset_management/src/domain/events"
	AssetRepository "asset_management/src/infrastructure/adapters"
	"asset_management/src/libs/logging"
)

func DeleteAssetCommand(c chan<- string, id string) {
	log := logger.GetLogger()

	log.Info().Str("id", id).Msg("deleting asset...")

	go AssetRepository.DeleteAsset(id)

	go DomainEvents.AssetDeleted(c, id)

	log.Info().Str("id", id).Msg("asset deleted...")
}
