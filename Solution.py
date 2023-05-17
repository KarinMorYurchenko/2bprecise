"""
Five critical tests:
1. When the request is successful, Verify the endpoint returns the status code 200 (OK)
2. Verify that each gene's allele information is contained in the response.
3. Verify whether the response contains only alleles for the specific gene and no other alleles.
4. Verify that no allele has an ethnicity frequency greater than one in the response.
5. Verify that no allele has a missing or null ethnicity frequency value.

Five additional tests:
1. The response must include the correct number of alleles for the specific gene.
2. In the CYC2D6 gene, verify that the response contains the expected allele information for specific alleles, such as 1, 2, etc.
3. Ensure that the response includes all the fields that have been expected, such as citations, evidence strength, or any other relevant information.
4. Test the pagination of the response, and if possible, retrieve additional pages.
5. Verify that the response includes headers such as the content type, caching directives,etc.

"""
import requests


def test_verify_that_each_ethnicity_frequency_is_lower_than_1_or_null():
    global request
    request = requests.session()
    cyc2d6_allele_data = request.get('https://api.cpicpgx.org/v1/allele?genesymbol=eq.CYP2D6&name=eq.*1').json()
    for allele in cyc2d6_allele_data:
        for ethnicity, frequency in allele["frequency"].items():
            assert frequency is None or frequency < 1, f"Invalid ethnicity frequency ({ethnicity}) for allele {allele['name']}"


def test_verify_the_sum_of_frequencies_in_all_cyp2d6_alleles_lower_than_1():
    request = requests.session()
    cyp2d6_allele_data = request.get('https://api.cpicpgx.org/v1/allele?genesymbol=eq.CYP2D6&name=eq.*1').json()
    ethnicity_frequencies = {}
    for allele in cyp2d6_allele_data:
        for ethnicity, frequency in allele["frequency"].items():
            if ethnicity not in ethnicity_frequencies:
                ethnicity_frequencies[ethnicity] = frequency
            else:
                ethnicity_frequencies[ethnicity] += frequency
    for ethnicity, total_frequency in ethnicity_frequencies.items():
        assert total_frequency < 1, f"Total frequency exceeds 1 for ethnicity'{ethnicity}'"


def test_verify_that_if_there_are_findings():
    request = requests.session()
    all_allele_data = request.get('https://api.cpicpgx.org/v1/allele').json()
    for allele in all_allele_data:
        print(allele['id'])
        findings = allele.get("findings")
        citations = allele.get("citations")
        strength = allele.get("strength")
        if findings:
            if citations is None:
                if strength == "No Evidence":
                    pass
                else:
                    print (allele['id'])
                    print("Conditions not satisfied: there are findings, then there is more than one citations OR the evidence strength is not 'No Evidence'.")
