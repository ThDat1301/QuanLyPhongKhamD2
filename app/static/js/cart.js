function addToReport(id, tenThuoc, donVi, donGia) {
    fetch('/api/add-medicines-to-report',
        {
            method: 'post',
            body: JSON.stringify({
                'id': id,
                'tenThuoc': tenThuoc,
                'donVi': donVi,
                'donGia': donGia,
                'cachDung': ""
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

function updateNumMedicines(id, obj) {
    fetch('/api/update-medicines', {
        method: 'put',
        body: JSON.stringify({
            'id': id,
            'soLuongThem': parseInt(obj.value)
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

function updateUseMedicines(id, obj) {
    fetch('/api/update-use-medicines', {
        method: 'put',
        body: JSON.stringify({
            'cachDung': obj.value
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

function deleteMedicines(id) {
    if (confirm("Bạn có muốn xoá thuốc ra khỏi danh sách hiện tại?") === true) {
        fetch('api/delete-medicines/' + id, {
            method: 'delete',
            headers: {
                'Content-Type': 'application/json'
            }

        }).then(function (res) {
            let medicine = document.getElementById("product" + id)
            medicine.style.display = "none"

        }).catch(function (err) {
            console.error(err)
        })
    }
}
