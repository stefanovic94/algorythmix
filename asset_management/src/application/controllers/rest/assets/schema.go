package assets

type CreateAsset struct {
	Symbol string `json:symbol validate:"required"`
}
