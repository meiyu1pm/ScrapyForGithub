# ScrapyForGithub
Based on the User-name, this script can collect the account email

### Script starting command:
`scrapy crawl git_spider -o evaluation.csv`
- Note:
    Please go for the path ../ScrapyForGithub/gitScrape/gitScrape/spiders directory and run the above command.
- It will output a csv file named evaluation.csv
- The noEmail.csv is I download from the company's mongoDB database that don't have possible_email or email fields.
