import request from '@/utils/request'

const api = {
  admissionPlan: '/api/admission-plan'
}

export function getAdmissionPlans(params) {
    console.log('Requesting admission plans with params:', params)  //添加日志
    return request({
      url: '/api/admission-catalogs/',
      method: 'get',
      params: params
    })
  }

export function getSubjects() {
    return request({
      url: '/api/admission-catalogs/get_subjects/',
      method: 'get'
    })
  }

export function getSubSubjects(parentId) {
    return request({
      url: '/api/admission-catalogs/get_sub_subjects/',
      method: 'get',
      params: { parent_id: parentId }
    })
  }

export function createAdmissionPlan (data) {
  return request({
    url: api.admissionPlan,
    method: 'post',
    data: data
  })
}

export function updateAdmissionPlan (id, data) {
  return request({
    url: `${api.admissionPlan}/${id}`,
    method: 'put',
    data: data
  })
}

export function deleteAdmissionPlan (id) {
  return request({
    url: `${api.admissionPlan}/${id}`,
    method: 'delete'
  })
}