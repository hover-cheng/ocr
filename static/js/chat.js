var vm = new Vue({
    el: '#app',
    data:{
        result: '',
        msg: '',
        butstatus: false,
        
    },
    methods: {
        clearmsg: function () {
            this.result = '';
            this.msg = '';
        },
        sendMsg: function () {
            msg = this.msg.trim();
            this.msg = '';
            if (msg == '') {
                alert('请输入内容...');
            } else {
            this.result += '问 ' +  msg + '\n';
            this.butstatus = true;
            axios.post('/chat', {'msg': msg})
            .then((res) => {
                this.result += '答 ' + res.data + '\n';
                this.butstatus = false;
            }).catch((err) => {
                console.log(err);
                this.butstatus = false;
            });
            }
        },
    }
});
