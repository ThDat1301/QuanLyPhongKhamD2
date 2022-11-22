function addToReport(id, tenThuoc, donVi, donGia) {
    fetch('/api/add-medicines-to-report',
        {
            method: 'post',
            body: JSON.stringify({
                'id': id,
                'tenThuoc': tenThuoc,
                'donVi': donVi,
                'donGia': donGia
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(function (res) {
            console.info(res)
            return res.json()
    }).then(function (data) {
        console.info(data)

    }).catch(function (err) {
        console.error(err)
    })
}