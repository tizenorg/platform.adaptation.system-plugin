/*-*- Mode: C; c-basic-offset: 8; indent-tabs-mode: nil -*-*/

/*
 * liblazymount
 *
 * Copyright (c) 2016 Samsung Electronics Co., Ltd.
 *
 * Licensed under the Apache License, Version 2.0 (the License);
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#ifndef _LAZY_MOUNT_H_
#define _LAZY_MOUNT_H_ 1
#ifdef __cplusplus
extern "C" {
#endif

/**
 * @brief Get the check value wheter system need the ui for lazy mount feature.
 * @return 1 if system should show the ui for lazy mount feature, otherwise 0.
 * @par Example
   @code
   #include <lazy_mount.h>

   int show_ui;

   show_ui = get_need_ui_for_lazy_mount();

   @endcode
 */
int get_need_ui_for_lazy_mount();

/**
 * @brief Create /tmp/.lazy_mount file to mount user partion to /opt/usr.
 * @return 0 if success to create /tmp/.lazy_mount, otherwise -errno.
 * @par Example
   @code
   #include <lazy_mount.h>

   int result;

   result = do_mount_user();

   @endcode
 */
int do_mount_user();

/**
 * @brief Wait for complete to mount user partion to /opt/usr.
 * @return 0 if success to mount it, otherwise -errno.
 * @par Example
   @code
   #include <lazy_mount.h>

   int result;

   result = wait_mount_user();

   @endcode
 */
int wait_mount_user();
#ifdef __cplusplus
extern "C" {
#endif

#endif // _LAZY_MOUNT_H_
