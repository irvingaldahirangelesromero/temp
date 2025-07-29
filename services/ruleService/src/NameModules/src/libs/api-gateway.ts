import HttpStatusCode from "../../../../../../src/shared/enums/httpStatusCode"

export const formatJSONResponse = (data, statusCode: HttpStatusCode = HttpStatusCode.OK) => {
  return {
    data,
    statusCode
  }
} 