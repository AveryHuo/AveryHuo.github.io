---
title: GAMES101作业笔记
cover: /img/160880489472852501.png
date: 2022-05-25 17:30:37
updated: 2022-08-23 16:10:01
top_img: false
categories:
- 图形学
tags: 
- 图形学
description: GAMES101作业笔记
keywords: "CG, 图形学"
---

#### 一、作业1
要求：
每次作业的评分，分为基础与提高两部分，即在作业批改时会给大家反馈两
个成绩。由于作业不是强制要求必须提交，所以在完成全部作业后，我们会统计
所有的基础分数。若基础分数及格则视为通过课程，反之视为不通过。
• [5 分] 正确构建模型矩阵。
• [5 分] 正确构建透视投影矩阵。
• [10 分] 你的代码可以在现有框架下正确运行，并能看到变换后的三角形。
• [10 分] 当按A 键与D 键时，三角形能正确旋转。或者正确使用命令行得
到旋转结果图像。
• [提高项5 分] 在main.cpp 中构造一个函数，该函数的作用是得到绕任意
过原点的轴的旋转变换矩阵。
Eigen::Matrix4f get_rotation(Vector3f axis, float angle)

```c++
//实现：

Eigen::Matrix4f get_model_matrix(Axis targetAxis, float rotation_angle)
{
    Eigen::Matrix4f model = Eigen::Matrix4f::Identity();

    float angle_rad = rotation_angle * MY_PI / 180.0;

    Eigen::Matrix4f model_trans;
    if (targetAxis == AxisZ) {
        model_trans <<
            cos(angle_rad), -sin(angle_rad), 0, 0,
            sin(angle_rad), cos(angle_rad), 0, 0,
            0, 0, 1, 0,
            0, 0, 0, 1;
    }else if (targetAxis == AxisY) {
        model_trans <<
            cos(angle_rad), 0, sin(angle_rad), 0,
            0, 1, 0, 0,
            -sin(angle_rad), 0, cos(angle_rad), 0,
            0, 0, 0, 1;
    }
    else if (targetAxis == AxisX) {
        model_trans <<
            1, 0, 0, 0,
            0, cos(angle_rad), -sin(angle_rad), 0,
            0, sin(angle_rad), cos(angle_rad), 0,
            0, 0, 0, 1;
    }
    

    model = model_trans * model;

    return model;
}

Eigen::Matrix4f get_projection_matrix(float eye_fov, float aspect_ratio,
                                      float zNear, float zFar)
{
    float eye_fov_rad = eye_fov * MY_PI / 180.0;
    Eigen::Matrix4f projection = Eigen::Matrix4f::Identity();

    // Calc to get l, r, t, b
    float l, r, t, b;
    t = -tan(eye_fov_rad) * zNear; //这里要取反方向，不然会转过来
    b = -t;
    l = t * aspect_ratio;
    r = -l;

    // Construct Matrix(persp-ortho) 挤压(透视)变换
    Eigen::Matrix4f matrix_p2o;
    matrix_p2o << 
        zNear, 0, 0, 0,
        0, zNear, 0, 0,
        0, 0, zNear+zFar, -zNear*zFar,
        0, 0, 1, 0;

    // Construct Matrix(orth) 正交变换矩阵,先平移，后缩放
    Eigen::Matrix4f matrix_orth, matrix_orth_move, matrix_orth_scale;
    matrix_orth_move << 
        1,0,0, -(r+l)/2,
        0,1,0, -(t+b)/2,
        0,0,1, -(zNear+zFar)/2,
        0,0,0,1;
    matrix_orth_scale <<
        2/(r-l), 0, 0, 0,
        0, 2/(t-b), 0, 0,
        0, 0, 2/(zNear-zFar),0,
        0,0,0,1;

    matrix_orth = matrix_orth_move * matrix_orth_scale;

    //Calc to the result
    projection = matrix_orth * matrix_p2o;

    return projection;
}

```

#### 二、作业2
要求
• [5 分] 正确地提交所有必须的文件，且代码能够编译运行。
• [20 分] 正确实现三角形栅格化算法。
• [10 分] 正确测试点是否在三角形内。
• [10 分] 正确实现z-buffer 算法, 将三角形按顺序画在屏幕上。
• [提高项5 分] 用super-sampling 处理Anti-aliasing : 你可能会注意
到，当我们放大图像时，图像边缘会有锯齿感。我们可以用super-sampling
来解决这个问题，即对每个像素进行2 * 2 采样，并比较前后的结果(这里
并不需要考虑像素与像素间的样本复用)。需要注意的点有，对于像素内的每
一个样本都需要维护它自己的深度值，即每一个像素都需要维护一个sample
list。最后，如果你实现正确的话，你得到的三角形不应该有不正常的黑边。

```c++
static bool insideTriangle(float x, float y, const Vector3f* _v)
{   
    //Implement this function to check if the point (x, y) is inside the triangle represented by _v[0], _v[1], _v[2]
    Vector2f vec1 = Vector2f(x - _v[0].x(), y - _v[0].y());
    Vector2f edge1 = Vector2f(_v[1].x() - _v[0].x(), _v[1].y() - _v[0].y());

    Vector2f vec2 = Vector2f(x - _v[1].x(), y - _v[1].y());
    Vector2f edge2 = Vector2f(_v[2].x() - _v[1].x(), _v[2].y() - _v[1].y());

    Vector2f vec3 = Vector2f(x - _v[2].x(), y - _v[2].y());
    Vector2f edge3 = Vector2f(_v[0].x() - _v[2].x(), _v[0].y() - _v[2].y());

    return vec1[0] * edge1[1] - vec1[1] * edge1[0] > 0
        && vec2[0] * edge2[1] - vec2[1] * edge2[0] > 0
        && vec3[0] * edge3[1] - vec3[1] * edge3[0] > 0;
}

void rst::rasterizer::rasterize_triangle(const Triangle& t) {
    auto v = t.toVector4();
    
    // TODO : Find out the bounding box of current triangle.
    int min_x = std::floor(std::min(v[0][0], std::min(v[1][0], v[2][0])));
    int max_x = std::ceil(std::max(v[0][0], std::max(v[1][0], v[2][0])));
    int min_y = std::floor(std::min(v[0][1], std::min(v[1][1], v[2][1])));
    int max_y = std::ceil(std::max(v[0][1], std::max(v[1][1], v[2][1])));

    bool useMSAA = true;
    int msaaRate = 2;
    if (useMSAA) {
        std::vector<Vector2f> pos;

        float cell_size = 1.0 / msaaRate;
        for(int i = 0; i < msaaRate; i++)
        {
            for (int j = 0; j < msaaRate; j++)
            {
                pos.push_back({cell_size * (float)j + 0.5 * cell_size, cell_size * (float)i + 0.5 * cell_size});
            }
        }

        int inside_counter = 0;
        float min_depth, alpha, beta, gamma;
        
        for (int x = min_x; x <= max_x; x++)
        {
            for (int y = min_y; y < max_y; y++)
            {
                min_depth = FLT_MAX;
                inside_counter = 0;
                for (int part = 0; part < msaaRate*2; part++) {
                    Vector2f cur_point;
                    cur_point << static_cast<float>(x + pos[part][0]), static_cast<float>(y + pos[part][1]);
                    if (insideTriangle(cur_point.x(), cur_point.y(), t.v)) {
                        auto tup = computeBarycentric2D(cur_point.x(), cur_point.y(), t.v);
                        std::tie(alpha, beta, gamma) = tup;
                        float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                        float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                        z_interpolated *= w_reciprocal;
                        min_depth = std::min(min_depth, z_interpolated);
                        inside_counter ++;
                    }
                }
                if (inside_counter > 0) {
                    if (depth_buf[get_index(x, y)] > min_depth) {
                        Vector3f point;
                        Eigen::Vector3f color = t.getColor() * inside_counter / (msaaRate * 2.0);
                        point << (float)x, (float)y, min_depth;
                        depth_buf[get_index(x, y)] = min_depth;
                        set_pixel(point, color);// 由count决定深浅
                    }
                }
            }
        }
    }
    else {
        float alpha, beta, gamma;
        for (int x = min_x; x <= max_x; x++)
        {
            for (int y = min_y; y < max_y; y++)
            {
                if (insideTriangle(static_cast<float>(x+0.5), static_cast<float>(y + 0.5), t.v)) {
                    auto tup = computeBarycentric2D(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v);
                    std::tie(alpha, beta, gamma) = tup;
                    float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                    float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                    z_interpolated *= w_reciprocal;

                    if (depth_buf[get_index(x, y)] > z_interpolated) {
                        Vector3f point;
                        point << static_cast<float>(x), static_cast<float>(y), z_interpolated;
                        depth_buf[get_index(x, y)] = z_interpolated;
                        set_pixel(point, t.getColor());
                    }
                }

            }
        }
    }
}


```

![效果对比](/img/160880489472852501.png) 


#### 三、作业3
要求：
• [5 分] 提交格式正确，包括所有需要的文件。代码可以正常编译、执行。
• [10 分] 参数插值: 正确插值颜色、法向量、纹理坐标、位置(Shading Position)
并将它们传递给fragment_shader_payload.
• [20 分]Blinn-phong 反射模型: 正确实现phong_fragment_shader 对应的
反射模型。
• [5 分] Texture mapping: 将phong_fragment_shader 的代码拷贝到
texture_fragment_shader, 在此基础上正确实现Texture Mapping.
• [10 分] Bump mapping 与Displacement mapping: 正确实现Bump mapping
与Displacement mapping.
7
• [Bonus 3 分] 尝试更多模型: 找到其他可用的.obj 文件，提交渲染结果并
把模型保存在/models 目录下。这些模型也应该包含Vertex Normal 信息。
• [Bonus 5 分] 双线性纹理插值: 使用双线性插值进行纹理采样, 在Texture
类中实现一个新方法Vector3f getColorBilinear(float u, float v) 并
通过fragment shader 调用它。为了使双线性插值的效果更加明显，你应该
考虑选择更小的纹理图。请同时提交纹理插值与双线性纹理插值的结果，并
进行比较。

> 向量点积对应到矩阵的点乘，是对应项的相乘之和。 向量叉乘对应矩阵间的m行与n列对应相乘之和成为新的m,n项（矩阵相乘），结果是一个新矩阵
> Eigen库的cwiseProduct实现了矩阵点积，即对应项相乘得到新的项，要求两个矩阵行列数要一样!

* rasterizer.cpp
```C++
//Screen space rasterization
void rst::rasterizer::rasterize_triangle(const Triangle& t, const std::array<Eigen::Vector3f, 3>& view_pos) 
{
    // TODO: From your HW3, get the triangle rasterization code.
    // TODO: Inside your rasterization loop:
    //    * v[i].w() is the vertex view space depth value z.
    //    * Z is interpolated view space depth for the current pixel
    //    * zp is depth between zNear and zFar, used for z-buffer

    // float Z = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
    // float zp = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
    // zp *= Z;

    // TODO: Interpolate the attributes:
    // auto interpolated_color
    // auto interpolated_normal
    // auto interpolated_texcoords
    // auto interpolated_shadingcoords

    // Use: fragment_shader_payload payload( interpolated_color, interpolated_normal.normalized(), interpolated_texcoords, texture ? &*texture : nullptr);
    // Use: payload.view_pos = interpolated_shadingcoords;
    // Use: Instead of passing the triangle's color directly to the frame buffer, pass the color to the shaders first to get the final color;
    // Use: auto pixel_color = fragment_shader(payload);

    auto v = t.toVector4();

    // TODO : Find out the bounding box of current triangle.
    int min_x = std::floor(std::min(v[0][0], std::min(v[1][0], v[2][0])));
    int max_x = std::ceil(std::max(v[0][0], std::max(v[1][0], v[2][0])));
    int min_y = std::floor(std::min(v[0][1], std::min(v[1][1], v[2][1])));
    int max_y = std::ceil(std::max(v[0][1], std::max(v[1][1], v[2][1])));

    int msaaRate = 2;
    float alpha, beta, gamma;
    for (int x = min_x; x <= max_x; x++)
    {
        for (int y = min_y; y < max_y; y++)
        {
            if (insideTriangle(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v)) {
                auto tup = computeBarycentric2D(static_cast<float>(x + 0.5), static_cast<float>(y + 0.5), t.v);
                std::tie(alpha, beta, gamma) = tup;
                float w_reciprocal = 1.0 / (alpha / v[0].w() + beta / v[1].w() + gamma / v[2].w());
                float z_interpolated = alpha * v[0].z() / v[0].w() + beta * v[1].z() / v[1].w() + gamma * v[2].z() / v[2].w();
                z_interpolated *= w_reciprocal;

                if (depth_buf[get_index(x, y)] > z_interpolated) {
                    // TODO: Interpolate the attributes:
                     auto interpolated_color = interpolate(alpha, beta, gamma, t.color[0], t.color[1], t.color[2], 1);
                     auto interpolated_normal = interpolate(alpha, beta, gamma, t.normal[0], t.normal[1], t.normal[2], 1).normalized();
                     auto interpolated_texcoords = interpolate(alpha, beta, gamma, t.tex_coords[0], t.tex_coords[1], t.tex_coords[2], 1);
                     auto interpolated_shadingcoords = interpolate(alpha, beta, gamma, view_pos[0], view_pos[1], view_pos[2], 1);

                    fragment_shader_payload payload( interpolated_color, interpolated_normal.normalized(), interpolated_texcoords, texture ? &*texture : nullptr);
                    payload.view_pos = interpolated_shadingcoords;
                    auto pixel_color = fragment_shader(payload);

                    depth_buf[get_index(x, y)] = z_interpolated;
                    set_pixel(Eigen::Vector2i(x, y), pixel_color);
                }
            }

        }
    }
}
```

* Texture.hpp
```c++
  Eigen::Vector3f getColor(float u, float v)
    {
        // 坐标限定
       /* if (u < 0) u = 0;
        if (u > 1) u = 1;
        if (v < 0) v = 0;
        if (v > 1) v = 1;*/

        if (u < 0 || u > 1 || v < 0 || v > 1)
            return Eigen::Vector3f(0,0,0);
        auto u_img = u * width;
        auto v_img = (1 - v) * height;
        auto color = image_data.at<cv::Vec3b>(v_img, u_img);
        return Eigen::Vector3f(color[0], color[1], color[2]);

    }

    Eigen::Vector3f getColorBilinear(float u, float v)
    {
        if (u < 0) u = 0;
        if (u > 1) u = 1;
        if (v < 0) v = 0;
        if (v > 1) v = 1;
        auto u_img = u * width;
        auto v_img = (1 - v) * height;

        float u_min = std::floor(u_img);
        float u_max = std::min((float)width, std::ceil(u_img));
        float v_min = std::floor(v_img);
        float v_max = std::min((float)height, std::ceil(v_img));

        auto Q11 = image_data.at<cv::Vec3b>(v_max, u_min);
        auto Q12 = image_data.at<cv::Vec3b>(v_max, u_max);

        auto Q21 = image_data.at<cv::Vec3b>(v_min, u_min);
        auto Q22 = image_data.at<cv::Vec3b>(v_min, u_max);

        float rs = (u_img - u_min) / (u_max - u_min);
        float rt = (v_img - v_max) / (v_min - v_max);
        auto cBot = (1 - rs) * Q11 + rs * Q12;
        auto cTop = (1 - rs) * Q21 + rs * Q22;
        auto P = (1 - rt) * cBot + rt * cTop;

        return Eigen::Vector3f(P[0], P[1], P[2]);
    }

```

* main.cpp - texture_fragment
```c++
Eigen::Vector3f texture_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f return_color = {0, 0, 0};
    if (payload.texture)
    {
        // TODO: Get the texture value at the texture coordinates of the current fragment
        return_color = payload.texture->getColor(payload.tex_coords.x(), payload.tex_coords.y());
    }
    Eigen::Vector3f texture_color;
    texture_color << return_color.x(), return_color.y(), return_color.z();

    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = texture_color / 255.f;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = texture_color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    Eigen::Vector3f result_color = {0, 0, 0};

    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
         // components are. Then, accumulate that result on the *result_color* object.
        Eigen::Vector3f light_dir = light.position - point;
        Eigen::Vector3f view_dir = eye_pos - point;
        float r = light_dir.dot(light_dir);
        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.normalized().dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.normalized().dot(h)), p);

        result_color += (La + Ld + Ls);

    }

    return result_color * 255.f;
}
```

* main.cpp - phong_fragment
```c++
Eigen::Vector3f phong_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{{20, 20, 20}, {500, 500, 500}};
    auto l2 = light{{-20, 20, 0}, {500, 500, 500}};

    std::vector<light> lights = {l1, l2};
    Eigen::Vector3f amb_light_intensity{10, 10, 10};
    Eigen::Vector3f eye_pos{0, 0, 10};

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    Eigen::Vector3f result_color = {0, 0, 0};
    for (auto& light : lights)
    {
        // 光的方向
        Eigen::Vector3f light_dir = light.position - point;
        // 视线方向
        Eigen::Vector3f view_dir = eye_pos - point;
        // 衰减因子
        float r = light_dir.dot(light_dir);

        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.normalized().dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.normalized().dot(h)), p);

        result_color += (La + Ld + Ls);
    }

    return result_color * 255.f;
}
```

* main.cpp - phong_fragment
```c++
Eigen::Vector3f displacement_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{ {20, 20, 20}, {500, 500, 500} };
    auto l2 = light{ {-20, 20, 0}, {500, 500, 500} };

    std::vector<light> lights = { l1, l2 };
    Eigen::Vector3f amb_light_intensity{ 10, 10, 10 };
    Eigen::Vector3f eye_pos{ 0, 0, 10 };

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;

    float kh = 0.2, kn = 0.1;

    // TODO: Implement displacement mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Position p = p + kn * n * h(u,v)
    // Normal n = normalize(TBN * ln)

    float x = normal.x();
    float y = normal.y();
    float z = normal.z();
    Eigen::Vector3f t{ x * y / std::sqrt(x * x + z * z), std::sqrt(x * x + z * z), z * y / std::sqrt(x * x + z * z) };
    Eigen::Vector3f b = normal.cross(t);
    Eigen::Matrix3f TBN;
    TBN << t.x(), b.x(), normal.x(),
        t.y(), b.y(), normal.y(),
        t.z(), b.z(), normal.z();

    float u = payload.tex_coords.x();
    float v = payload.tex_coords.y();
    float w = payload.texture->width;
    float h = payload.texture->height;


    float dU = kh * kn * (payload.texture->getColor(u + 1.0f / w, v).norm() - payload.texture->getColor(u, v).norm());
    float dV = kh * kn * (payload.texture->getColor(u, v + 1.0f / h).norm() - payload.texture->getColor(u, v).norm());

    Eigen::Vector3f ln{ -dU,-dV,1.0f };

    point += (kn * normal * payload.texture->getColor(u, v).norm());

    normal = TBN * ln;
    normal = normal.normalized();

    Eigen::Vector3f result_color = { 0, 0, 0 };

    for (auto& light : lights)
    {
        // TODO: For each light source in the code, calculate what the *ambient*, *diffuse*, and *specular* 
        // components are. Then, accumulate that result on the *result_color* object.
        Eigen::Vector3f light_dir = light.position - point;
        Eigen::Vector3f view_dir = eye_pos - point;
        float r = light_dir.dot(light_dir);

        // ambient
        Eigen::Vector3f La = ka.cwiseProduct(amb_light_intensity);
        // diffuse
        Eigen::Vector3f Ld = kd.cwiseProduct(light.intensity / r);
        Ld *= std::max(0.0f, normal.dot(light_dir.normalized()));
        // specular
        Eigen::Vector3f h = (light_dir + view_dir).normalized();
        Eigen::Vector3f Ls = ks.cwiseProduct(light.intensity / r);
        Ls *= std::pow(std::max(0.0f, normal.dot(h)), p);

        result_color += (La + Ld + Ls);

    }

    return result_color * 255.f;
}
```


* main.cpp - bump_fragment
```c++
Eigen::Vector3f bump_fragment_shader(const fragment_shader_payload& payload)
{
    Eigen::Vector3f ka = Eigen::Vector3f(0.005, 0.005, 0.005);
    Eigen::Vector3f kd = payload.color;
    Eigen::Vector3f ks = Eigen::Vector3f(0.7937, 0.7937, 0.7937);

    auto l1 = light{ {20, 20, 20}, {500, 500, 500} };
    auto l2 = light{ {-20, 20, 0}, {500, 500, 500} };

    std::vector<light> lights = { l1, l2 };
    Eigen::Vector3f amb_light_intensity{ 10, 10, 10 };
    Eigen::Vector3f eye_pos{ 0, 0, 10 };

    float p = 150;

    Eigen::Vector3f color = payload.color;
    Eigen::Vector3f point = payload.view_pos;
    Eigen::Vector3f normal = payload.normal;


    float kh = 0.2, kn = 0.1;

    // TODO: Implement bump mapping here
    // Let n = normal = (x, y, z)
    // Vector t = (x*y/sqrt(x*x+z*z),sqrt(x*x+z*z),z*y/sqrt(x*x+z*z))
    // Vector b = n cross product t
    // Matrix TBN = [t b n]
    // dU = kh * kn * (h(u+1/w,v)-h(u,v))
    // dV = kh * kn * (h(u,v+1/h)-h(u,v))
    // Vector ln = (-dU, -dV, 1)
    // Normal n = normalize(TBN * ln)

    float x = normal.x();
    float y = normal.y();
    float z = normal.z();
    Eigen::Vector3f t{ x * y / std::sqrt(x * x + z * z), std::sqrt(x * x + z * z), z * y / std::sqrt(x * x + z * z) };
    Eigen::Vector3f b = normal.cross(t);
    Eigen::Matrix3f TBN;
    TBN << t.x(), b.x(), normal.x(),
        t.y(), b.y(), normal.y(),
        t.z(), b.z(), normal.z();

    float u = payload.tex_coords.x();
    float v = payload.tex_coords.y();
    float w = payload.texture->width;
    float h = payload.texture->height;

    float dU = kh * kn * (payload.texture->getColor(u + 1.0f / w, v).norm() - payload.texture->getColor(u, v).norm());
    float dV = kh * kn * (payload.texture->getColor(u, v + 1.0f / h).norm() - payload.texture->getColor(u, v).norm());

    Eigen::Vector3f ln{ -dU,-dV,1.0f };

    normal = TBN * ln;
    // 归一化
    Eigen::Vector3f result_color = normal.normalized();
    return result_color * 255.f;
}
```

#### 四、作业4
需要实现 de Casteljau 算法来绘制由 4 个控制点表示的 Bézier 曲线 (当你正确实现该
算法时，你可以支持绘制由更多点来控制的 Bézier 曲线)。
你需要修改的函数在提供的 main.cpp 文件中。
• bezier：该函数实现绘制 Bézier 曲线的功能。它使用一个控制点序列和一个
OpenCV：：Mat 对象作为输入，没有返回值。它会使 t 在 0 到 1 的范围内进
行迭代，并在每次迭代中使 t 增加一个微小值。对于每个需要计算的 t，将
调用另一个函数 recursive_bezier，然后该函数将返回在 Bézier 曲线上 t
处的点。最后，将返回的点绘制在 OpenCV ：：Mat 对象上。
• recursive_bezier：该函数使用一个控制点序列和一个浮点数 t 作为输入，
实现 de Casteljau 算法来返回 Bézier 曲线上对应点的坐标。

要求：
• [20 分] De Casteljau 算法：
对于给定的控制点，你的代码能够产生正确的 Bézier 曲线。
• [5 分] 奖励分数：
实现对 Bézier 曲线的反走样。(对于一个曲线上的点，不只把它对应于一个像
素，你需要根据到像素中心的距离来考虑与它相邻的像素的颜色。)

可能会有的问题：需要对每一个点进行差值
``` c++
cv::Point2f recursive_bezier(const std::vector<cv::Point2f>& control_points, float t)
{
    // TODO: Implement de Casteljau's algorithm

    if (control_points.size() == 0) {
        // Error!!
        return cv::Point2f();
    }
    else if (control_points.size() == 1) {
        return control_points[0];
    }
    else{
        std::vector<cv::Point2f> points;
        for (size_t i = 0; i < control_points.size() - 1; i++)
        {
            points.push_back(control_points[i] + (control_points[i+1] - control_points[i]) * t);
        }
        return recursive_bezier(points, t);
    }
    
    return cv::Point2f();

}

void bezier(const std::vector<cv::Point2f> &control_points, cv::Mat &window) 
{
    // TODO: Iterate through all t = 0 to t = 1 with small steps, and call de Casteljau's 
    // recursive Bezier algorithm.
    for (double t = 0.0; t <= 1.0; t += 0.001)
    {
        auto point = recursive_bezier(control_points, t);
        window.at<cv::Vec3b>(point.y, point.x)[1] = 255;

        std::vector<cv::Point2f> points(4);
        points[0] = cv::Point2f(std::floor(point.x + 0.5), std::floor(point.y + 0.5));
        points[1] = cv::Point2f(std::floor(point.x + 0.5), std::floor(point.y - 0.5));
        points[2] = cv::Point2f(std::floor(point.x - 0.5), std::floor(point.y + 0.5));
        points[3] = cv::Point2f(std::floor(point.x - 0.5), std::floor(point.y - 0.5));
    
        cv::Point2f distance = points[0] - point; //距离采样点最近的像素点坐标是+0.5后的点
        float d0 = sqrt(distance.x * distance.x + distance.y * distance.y); //取这个距离作为参照
        
        for (auto p : points)
        {
            
            cv::Point2f d = p - point;
            float percnet = d0 / sqrt(d.x * d.x + d.y * d.y); //计算其他像素点与最近距离的比值
            float color = window.at<cv::Vec3b>(p.y, p.x)[1];
            color = std::max(color, 255 * percnet);//取最大值效果更好
            window.at<cv::Vec3b>(p.y, p.x)[1] = color;
        }
    }
}
```

