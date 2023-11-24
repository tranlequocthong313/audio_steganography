function download(activeTab, filename) {
    fetch(`/download/${activeTab}/${filename}`, {
        method: 'GET'
    })
        .then(res => {
            return res.blob()
        })
        .then(blob => {
            const blobUrl = URL.createObjectURL(blob)
            const a = document.createElement('a')
            a.href = blobUrl
            a.download = filename
            document.body.appendChild(a)
            a.click()
            document.body.removeChild(a)
            URL.revokeObjectURL(blobUrl)
        })
        .catch(e => {
            console.log(e)
        })
        .finally(() => {
            location.reload()
        })
}

function showProgress() {
    document.querySelector('form').style.display = 'none'
    document.querySelector('.loading').style.display = 'block'
    document.querySelector('form').submit()
}
