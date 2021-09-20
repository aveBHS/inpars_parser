import cv2


def blur_logos_background(image, logos_top_border, logos_left_border, width, length, anchor=(20, 20)):
    image[logos_top_border: width + logos_top_border, logos_left_border: logos_left_border + length, :] = \
        cv2.blur(image[logos_top_border: width + logos_top_border,
                 logos_left_border: logos_left_border + length, :],
                 anchor, cv2.BORDER_CONSTANT)

    return image


def multiple_images(image, shape):
    """
    изменяет размеры картинкы и повторяет туже картинку.
    используется только для картинок с gipernn.ru
    :param image: картинка которая должна быть изменена
    :param shape: размеры итоговой картинкы
    :return: итоговая картинка
    """
    count_rows = shape[0] // image.shape[0] - 1
    count_columns = shape[1] // image.shape[1] - 1
    output_image = image
    for _ in range(count_rows):
        output_image = cv2.vconcat([output_image, image])

    output_image = cv2.vconcat([output_image, image[:(shape[0] - output_image.shape[0]), :, :]])

    image = output_image

    for _ in range(count_columns):
        output_image = cv2.hconcat([output_image, image])

    output_image = cv2.hconcat([output_image, image[:, :(shape[1] - output_image.shape[1]), :]])

    return output_image


def set_watermark(background_image, source_website, big_logo_path, small_logo_path):
    """
    подстовляет логотип зависив от сайта с которой взят бэкграунд
    :param background_image: картинка на которой должен ставиться логотип
    :param source_website: имя сайта источника
    (avito.ru, cian.ru, irr.ru, youla.io, sob.ru, bazarpnz.ru, kupiprodai.ru,
    move.ru, realty.yandex.ru, moyareklama.ru, dom.sakh.com, gipernn.ru, mlsn.ru, orsk.ru)
    :param big_logo_path: ссылка на картинку болшого логотипа
    :param small_logo_path: ссылка на картинку маленького логотипа
    :return: картинка с новым логотипом
    """
    overlay_image = None
    alpha = 0.0
    beta = 0.0
    if source_website == "avito.ru":
        logo = cv2.imread(big_logo_path)
        logo_width = min(int(background_image.shape[1] * 0.6), background_image.shape[0] // 2)
        logo_length = int(3 * background_image.shape[1] / 4)
        logo = cv2.resize(logo, (logo_length, logo_width))

        logo_top_border = (background_image.shape[0] - logo.shape[0]) // 2
        logo_bottom_border = background_image.shape[0] - ((background_image.shape[0] + logo.shape[0]) // 2)
        logo_left_border = (background_image.shape[1] - logo.shape[1]) // 2
        logo_right_border = background_image.shape[1] - ((background_image.shape[1] + logo.shape[1]) // 2)
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.7
        beta = 1.2

    elif source_website == 'cian.ru':
        logo = cv2.imread(small_logo_path)
        logo_width = background_image.shape[0] // 4
        logo_length = background_image.shape[1] // 3
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = background_image.shape[0] - logo.shape[0] - 10
        logo_bottom_border = 10
        logo_left_border = background_image.shape[1] - logo.shape[1] - 50
        logo_right_border = 50
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.8
        beta = 2

    elif source_website == "irr.ru" or source_website == "kupiprodai.ru":
        logo = cv2.imread(small_logo_path)
        logo_width = min(224, background_image.shape[0] // 5)
        logo_length = min(300, background_image.shape[1] // 2)
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = background_image.shape[0] - logo.shape[0]
        logo_bottom_border = 0
        logo_left_border = background_image.shape[1] - logo.shape[1]
        logo_right_border = 0
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(
            logo, logo_top_border,
            logo_bottom_border, logo_left_border, logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.9
        beta = 2.0

    elif source_website == "youla.io" or source_website == "sob.ru" or source_website == "mlsn.ru":
        logo = cv2.imread(big_logo_path)
        logo_width = min(100, background_image.shape[0])
        logo_length = min(200, background_image.shape[1])
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = background_image.shape[0] - logo.shape[0]
        logo_bottom_border = 0
        logo_left_border = background_image.shape[1] - logo.shape[1]
        logo_right_border = 0
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(logo,
                                           logo_top_border,
                                           logo_bottom_border,
                                           logo_left_border,
                                           logo_right_border,
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 0.7

    elif source_website == "bazarpnz.ru":
        logo = cv2.imread(small_logo_path)
        logo_width = 266
        logo_length = 450
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = (background_image.shape[0] - logo.shape[0]) // 2
        logo_bottom_border = background_image.shape[0] - ((background_image.shape[0] + logo.shape[0]) // 2)
        logo_left_border = (background_image.shape[1] - logo.shape[1]) // 2
        logo_right_border = background_image.shape[1] - ((background_image.shape[1] + logo.shape[1]) // 2)
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 1.0
        beta = 1.2

    elif source_website == "move.ru":
        logo = cv2.imread(big_logo_path)
        logo_width = min(background_image.shape[0], 100)
        logo_length = min(background_image.shape[1], 225)
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = background_image.shape[0] - logo.shape[0]
        logo_bottom_border = 0
        logo_left_border = background_image.shape[1] - logo.shape[1]
        logo_right_border = 0
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length, anchor=(40, 40))
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 0.9
        beta = 2.0

    elif source_website == "realty.yandex.ru":
        logo = cv2.imread(small_logo_path)
        logo_width = min(background_image.shape[0], 70)
        logo_length = min(background_image.shape[1], 220)
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = 0
        logo_bottom_border = background_image.shape[0] - logo.shape[0]
        logo_left_border = 0
        logo_right_border = background_image.shape[1] - logo.shape[1]
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length, anchor=(40, 40))
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border,
                                           logo_left_border, logo_right_border,
                                           cv2.BORDER_CONSTANT, (0, 0, 0))

        alpha = 1.0
        beta = 2.0

    elif source_website == "moyareklama.ru":
        logo = cv2.imread(big_logo_path)
        logo_width = min(background_image.shape[0], 150)
        logo_length = min(background_image.shape[1], 231)
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = (background_image.shape[0] - logo.shape[0]) // 2
        logo_bottom_border = background_image.shape[0] - ((background_image.shape[0] + logo.shape[0]) // 2)
        logo_left_border = (background_image.shape[1] - logo.shape[1]) // 2
        logo_right_border = background_image.shape[1] - ((background_image.shape[1] + logo.shape[1]) // 2)
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length, anchor=(30, 30))
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border,
                                           logo_left_border, logo_right_border,
                                           cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 1.0

    elif source_website == "dom.sakh.com":
        logo = cv2.imread(big_logo_path)
        logo_width = background_image.shape[0] // 4
        logo_length = min(background_image.shape[1], int(background_image.shape[0]))
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = 3 * (background_image.shape[0] - logo.shape[0]) // 4
        logo_bottom_border = background_image.shape[0] - logo.shape[0] - \
                             3 * (background_image.shape[0] - logo.shape[0]) // 4
        logo_left_border = (background_image.shape[1] - logo.shape[1]) // 2
        logo_right_border = background_image.shape[1] - ((background_image.shape[1] + logo.shape[1]) // 2)
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length, anchor=(50, 50))
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 1.2

    # elif source_website == "gipernn.ru":
    #     logo = cv2.imread(big_logo_path)
    #     logo_width = 350
    #     logo_length = 200
    #     logo = cv2.resize(logo, (logo_length, logo_width))
    #     logo_top_border = 0
    #     logo_bottom_border = 0
    #     logo_left_border = 70
    #     logo_right_border = 0
    #     background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
    #                                              logo_width, logo_length, anchor=(50, 50))
    #     logo = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
    #                               logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))
    #     overlay_image = multiple_images(logo, background_image.shape)
    #
    #     alpha = 1.0
    #     beta = 1.5

    elif source_website == "orsk.ru":
        logo = cv2.imread(big_logo_path)
        logo_width = background_image.shape[0] // 4
        logo_length = min(background_image.shape[1], 355)
        logo = cv2.resize(logo, (logo_length, logo_width))
        logo_top_border = (background_image.shape[0] - logo.shape[0]) // 2
        logo_bottom_border = background_image.shape[0] - ((background_image.shape[0] + logo.shape[0]) // 2)
        logo_left_border = (background_image.shape[1] - logo.shape[1]) // 2
        logo_right_border = background_image.shape[1] - ((background_image.shape[1] + logo.shape[1]) // 2)
        background_image = blur_logos_background(background_image, logo_top_border, logo_left_border,
                                                 logo_width, logo_length)
        overlay_image = cv2.copyMakeBorder(logo, logo_top_border, logo_bottom_border, logo_left_border,
                                           logo_right_border, cv2.BORDER_CONSTANT, (0, 0, 0))
        alpha = 1.0
        beta = 0.8

    result = cv2.addWeighted(background_image, alpha, overlay_image, beta, 0)
    return result
