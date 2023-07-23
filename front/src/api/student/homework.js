import * as axios from "@/common/myAxios";

export const submitHomework = studentHomework => {
    // 使用form表单的数据格式
    const params = new FormData()
    // 将上传文件数组依次添加到参数paramsData中
    studentHomework.fileList.forEach((x) => {
      params.append('file', x.file)
    });
    // 将输入表单数据添加到params表单中
    params.append('homeworkId', this.importForm.homeworkId)
    params.append('homeworkTitle', this.importForm.homeworkTitle)
    params.append('homeworkContent', this.importForm.homeworkContent)
    params.append('title', this.importForm.title)
    params.append('content', this.importForm.content)
    return axios.post("/student/homework/", studentHomework, {
	        	headers: {'content-type': 'multipart/form-data'}
	        });
}

export const getHomework = homeworkId => axios.get("/student/homework/" + homeworkId);

export const getPageCount = (homeworkId, homeworkTitle) => axios.get("/student/homework/page/count", {
    homeworkId: homeworkId,
    homeworkTitle: homeworkTitle
});

export const getPage = (index, homeworkId, homeworkTitle) => axios.get("/student/homework/page/" + index, {
    homeworkId: homeworkId,
    homeworkTitle: homeworkTitle
});

export const pageSize = 7;