package events

import "asset_management/src/domain/entities"

type AssetCreatedEventData struct {
	ID     string
	Symbol string
}

func AssetCreated(c chan<- entities.Asset, obj entities.Asset) {
	c <- obj
}
