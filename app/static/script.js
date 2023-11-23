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
            location.reload()
        })
}

