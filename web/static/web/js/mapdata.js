async function getCases() {
    try {
        cases = await axios.get('/api/cases');
        hospitals = await axios.get('/api/hospitals');
        provinces = await axios.get('https://raw.githubusercontent.com/macoymejia/geojsonph/master/Province/Provinces.json');
        metro = await axios.get('https://raw.githubusercontent.com/macoymejia/geojsonph/master/Philippines/Luzon/Metropolitant%20Manila/MetropolitantManila.json');

        console.log(`Request for "cases" completed with code ${cases.request.status}`);
        console.log(`Request for "hospitals" completed with code ${hospitals.request.status}`);
        console.log(`Request for "provinces" completed with code ${provinces.request.status}`);
        console.log(`Request for "metro" completed with code ${metro.request.status}`);
    } catch (err) {
        console.log(err);
    }
}

getCases();
