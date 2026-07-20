from predict import predict_house_price

sample_house = {
    "OverallQual": 7,
    "GrLivArea": 1710,
    "TotalBsmtSF": 856,
    "2ndFlrSF": 854,
    "BsmtFinSF1": 706,
    "1stFlrSF": 856,
    "LotArea": 8450,
    "GarageArea": 548
}

prediction = predict_house_price(sample_house)

print(f"Predicted House Price: {prediction}")