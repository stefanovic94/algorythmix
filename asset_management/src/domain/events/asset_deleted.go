package events

func AssetDeleted(c chan<- string, id string) {
	c <- id
}
