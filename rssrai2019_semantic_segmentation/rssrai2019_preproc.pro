function check_path, pathname
  if ~file_test(pathname, /directory) then begin
    file_mkdir, pathname
    print, pathname + ' has been created!'
  endif else begin
    file_delete, pathname
    file_mkdir, pathname
    print, pathname + ' has been reset!'
  endelse
end

function generate_baselist, img_path, suffix
  full_suffix = '*.' + suffix
  basename_list = file_basename(file_search(img_path, full_suffix))
  return, basename_list
end

function generate_list, img_path, basename_list, suffix
  file_count = size(basename_list, /n_elements)
  filename_list = strarr(file_count)
  foreach basename, basename_list, index do begin
    filename_list[index] = img_path + path_sep() + strmid(basename, 0, strlen(basename) - 3) + suffix
  endforeach
  return, filename_list
end

function preproc_batch, img_filename_list, output_filename_list
  file_count = size(img_filename_list, /n_elements)
  for i = 0, file_count - 1 do begin
    print, 'Index: ', i
    img_filename = img_filename_list[i]
    output_filename = output_filename_list[i]
    print, ' Reading: ', img_filename
    img = read_image(img_filename)
    print, ' Writing: ', output_filename
    write_image, output_filename, 'TIFF', img
  endfor
  print, 'Done!'
end

pro rssrai_preproc, img_path, img_suffix, output_path, output_suffix
  void = check_path(output_path)
  basename_list = generate_baselist(img_path, img_suffix)
  img_filename_list = generate_list(img_path, basename_list, img_suffix)
  output_filename_list = generate_list(output_path, basename_list, output_suffix)
  void = preproc_batch(img_filename_list, output_filename_list)
end