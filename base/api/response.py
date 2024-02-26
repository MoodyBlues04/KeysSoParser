class RsyaAdsResponse:
    def __init__(self, response: dict):
        self.__validate(response)

        self.current_page = response['current_page']
        self.per_page = response['per_page']
        self.last_page = response['last_page']
        self.data = response['data']

    def __validate(self, response: dict):
        required = ['current_page', 'per_page', 'last_page', 'data']
        for field in required:
            if response.get(field) is None:
                raise Exception(f'Invalid response. Field: {field} not specified')
