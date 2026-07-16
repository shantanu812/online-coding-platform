class OutputComparator:
   
    @staticmethod
    def compare(
        expected: str,
        actual: str,
    ) -> bool:
        return (
            expected.strip()
            == actual.strip()
        )