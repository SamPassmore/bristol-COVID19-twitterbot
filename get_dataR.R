endpoint <- 'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=ltla;areaCode=E06000023&structure={"date":"date","areaName":"areaName","areaCode":"areaCode","newCasesBySpecimenDate":"newCasesBySpecimenDate","cumCasesBySpecimenDate":"cumCasesBySpecimenDate","cumCasesBySpecimenDateRate":"cumCasesBySpecimenDateRate","cumTestsByPublishDate":"cumTestsByPublishDate"}'

# endpoint <- 'https://api.coronavirus.data.gov.uk/v1/data?filters=areaType=nhsRegion&structure={"date":"date"}}'

httr::GET(
  url = endpoint,
  httr::timeout(10)
) -> response


if (response$status_code >= 400) {
  err_msg = httr::http_status(response)
  stop(err_msg)
}

# Convert response from binary to JSON:
json_text <- httr::content(response, "text")
data      <- jsonlite::fromJSON(json_text)

# head(data$data)

write(json_text, '~/Projects_Git/bristol-covid10-twitterbot/data.json')
