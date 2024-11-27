package assets

type CreateAsset struct {
	Symbol string `json:symbol validate:"required"`
}

type AssetResponse struct {
	ID                  string `json:"id"`
	Symbol              string `json:"symbol"`
	ShortName           string `json:"short_name"`
	LongName            string `json:"long_name"`
	City                string `json:"city"`
	State               string `json:"state"`
	Country             string `json:"country"`
	Sector              string `json:"sector"`
	Industry            string `json:"industry"`
	LongBusinessSummary string `json:"long_business_summary"`
}
