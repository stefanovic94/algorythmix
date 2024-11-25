package events

import "asset_management/src/domain/entities"

type AssetCreatedEventData struct {
	ID     string
	symbol string
}

func AssetCreated(c chan<- entities.Asset, obj entities.Asset) {
	c <- obj
}
