var vm = new Vue({
  el: '#app',
  data: {
    files: null,
    imgname : null,
    imageUrl: null,
    imageSrc: null,
    display: "none",
    result: [],
    butstatus: false,
    selectedLang: 'ch',
  },
  methods: {
    handleFiles: function(e) {
      this.files = e.target.files[0];
      this.imgname = this.files.name;
    },
    uploadImage: function() {
      this.result = [];
      if (this.files) {
        this.butstatus = true;
        var reader = new FileReader();
        // 创建一个 FormData 对象
        var formData = new FormData();
          // 用于读取文件
          reader.onload = (e) => {
            this.imageSrc = e.target.result;
            this.display = "block";
          };

          reader.readAsDataURL(this.files);
          
          // 将文件添加到 FormData 对象中
          formData.append('image', this.files);
          formData.append('name', this.imgname);
          formData.append('lang', this.selectedLang);
          // 将 FormData 对象发送到服务器
          axios.post('/upload', formData, {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          })
          .then(res => {
            this.result = res.data.result;
            this.butstatus = false;
            console.log(this.result);
          })
          .catch(error => {
            this.butstatus = false;
            // 处理错误
            console.log(error);
          });
        } else {
          console.log(this.selectedLang);
          alert('Please select an image to upload.');
        }
      },
  }
});