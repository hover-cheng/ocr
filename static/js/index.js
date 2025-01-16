/*jshint esversion: 6 */
var vm = new Vue({
  el: '#app',
  data:{
    envirs: [
      {name: 'up1Uat', url: '192.168.104.147:8888'},
      {name: 'up1Map', url: '192.168.104.180:8888'},
      {name: 'up1Pre', url: '192.168.104.181:8888'},
      {name: 'up1Test', url: '192.168.82.46:8888'},
      {name: 'up3Pre', url: '192.168.104.181:8888'},
    ],
    commandList: [
      {name: '查看开关值', 0: ['/call/GmService/list_switches?args=%5B%22hall%22%5D'], 1: ['/call/GmService/list_switches?args=%5B%22hall%22%5D']},
      {name: '地区检测', 0: ['/call/GmService/change_switch?args=%5B%22ENABLE_LOGIN_VALIDATION%22%2C%221%22%2C%22hall%22%5D'], 1: ['/call/GmService/change_switch?args=%5B%22ENABLE_LOGIN_VALIDATION%22%2C%220%22%2C%22hall%22%5D']},
      {name: '白名单', 0: ['/call/GmService/change_switch?args=%5B%22ENABLE_WHITE_LIST%22%2C%221%22%2C%22hall%22%5D'], 1: ['/call/GmService/change_switch?args=%5B%22ENABLE_WHITE_LIST%22%2C%220%22%2C%22hall%22%5D']},
      {name: '激活', 0: ['/call/GmService/change_switch?args=%5B%22ENABLE_ACTIVATION%22%2C%221%22%2C%22hall%22%5D', '/call/GmService/change_switch?args=%5B%22ENABLE_ACTIVATION%22%2C%221%22%2C%22ms%22%5D'] , 1: ['/call/GmService/change_switch?args=%5B%22ENABLE_ACTIVATION%22%2C%220%22%2C%22hall%22%5D', '/call/GmService/change_switch?args=%5B%22ENABLE_ACTIVATION%22%2C%220%22%2C%22ms%22%5D']},
    ],
    arr1: ["zero","one","two","three","four","five","six","seven","eight","nine"],
    selectStatus: false,
    selectName: '',
    selectUrl: '',
    checkedValue: [],
    devUrl: 'http://192.168.101.39:8080',
    envirsNum: "ui ten item menu",
    result: '',
  },
  methods: {
    selectRegion: function(id) {
      this.selectStatus = true;
      this.result = '';
      this.selectName = this.envirs[id].name;
      this.selectUrl = this.envirs[id].url;
    },
    reslog: function(res) {
      console.log(res.data);
    },
    getItemNum: function() {
      if ( this.envirs.length <= 10) {
        this.envirsNum = "ui " + this.arr1[this.envirs.length] + " item menu";
      } else {
        this.envirsNum = "ui ten item menu";
      }
    },

    checkCommand: function(id, status) {
      const url = this.commandList[id][status];
      this.checkedValue = [];
      if (url.length == 1) {
        this.checkedValue.push("http://" + this.selectUrl + url[0]);
      } else {
        for (let i=0;i<url.length;i++) {
          this.checkedValue.push("http://" + this.selectUrl + url[i]);
        }
      }
      for (let i=0; i<this.checkedValue.length; i++) {
        axios.get(this.devUrl + '/todo' + '?url=' + this.checkedValue[i])
        .then(response=>{
                this.result = response.data.data;
                this.reslog(response);
              })
        .catch(error=>this.reslog(error));
      }
    },
    getResult: function() {
      axios.get("http://7.61.99.27:61003/details")
        .then(response=>{
                this.result = response.data.data;
                this.reslog(response);
              })
        .catch(error=>this.reslog(error));
    }
  },
  mounted: function() {
    this.getItemNum();
  },
});
