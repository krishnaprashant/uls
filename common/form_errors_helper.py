from bs4 import BeautifulSoup



def extractErrors(errorHtml):
    errors_list = {}
    soup = BeautifulSoup(str(errorHtml),'lxml')
    errors = soup.get_text(separator=',')
    errors = errors.split(".,")
    for err in errors:
        error = err.split(",")
        error_name = error[0]
        error_value = error[1]
        errors_list[error_name] = error_value
    return errors_list