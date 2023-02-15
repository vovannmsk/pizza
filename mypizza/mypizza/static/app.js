new Vue({
    el: '#list_apps',
    data: {
    products: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/list2/').then(function(response){
            console.log(response.data);
        })

    }
})