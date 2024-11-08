import request from '@/utils/request'

export function getSubjects() {
  return request({
    url: '/api/admission-catalogs/get_subjects/',
    method: 'get'
  })
}

export function getSubSubjects(parentId) {
  console.log('Requesting sub subjects with parentId:', parentId) // 调试日志
  return request({
    url: '/api/admission-catalogs/get_sub_subjects/',
    method: 'get',
    params: { parent_id: parentId }
  })
}