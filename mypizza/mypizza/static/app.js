new Vue({
    el: '#list_apps',
    data: {
    products: []
    },
    created: function () {
        const vm = this;
        axios.get('/api/list/').then(function (response){
        vm.products = response.data
        })
    }
})