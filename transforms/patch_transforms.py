def centered_patch_transform(patch_size=(1024, 1024)):
    def perform(image_tensor, item):
        image_shape = image_tensor.shape

        cx = item['cx']
        cy = item['cy']

        minx_naive = int(cx - patch_size[0] / 2)
        minx = max((0, minx_naive))
        dx1 = minx_naive - minx

        maxx_naive = int(cx + patch_size[0] / 2)
        maxx = min((maxx_naive, image_shape[1]))
        dx2 = maxx - maxx_naive

        if dx1 != 0 and dx2 != 0:
            print('Warning: patch size bigger than image x-dimension. Please select a smaller patch size.')
        else:
            minx -= dx2
            maxx -= dx1

        miny_naive = int(cy - patch_size[1] / 2)
        miny = max((0, miny_naive))
        dy1 = miny_naive - miny

        maxy_naive = int(cy + patch_size[1] / 2)
        maxy = min((maxy_naive, image_shape[0]))
        dy2 = maxy - maxy_naive

        if dy1 != 0 and dy2 != 0:
            print('Warning: patch size bigger than image y-dimension. Please select a smaller patch size.')
        else:
            miny -= dy2
            maxy -= dy1

        image_tensor = image_tensor[miny: maxy, minx: maxx]

        return image_tensor, item

    return perform