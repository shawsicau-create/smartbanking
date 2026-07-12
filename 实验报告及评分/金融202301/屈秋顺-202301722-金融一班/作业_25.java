package com.example.crm.controller;

import com.example.crm.dto.response.ApiResponse;
import com.example.crm.entity.Customer;
import com.example.crm.service.CustomerService;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.domain.Sort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

/**
 * 客户管理控制器
 */
@RestController
@RequestMapping("/api/customers")
@RequiredArgsConstructor
@Slf4j
public class CustomerController {

    private final CustomerService customerService;

    /**
     * 查询客户列表
     *
     * @param page  页码
     * @param size  每页数量
     * @param name  客户姓名
     * @param phone 联系电话
     * @param level 客户等级
     * @return 客户分页列表
     */
    @GetMapping
    public ResponseEntity<ApiResponse<Page<Customer>>> listCustomers(
            @RequestParam(defaultValue = "0") int page,
            @RequestParam(defaultValue = "10") int size,
            @RequestParam(required = false) String name,
            @RequestParam(required = false) String phone,
            @RequestParam(required = false) String level) {
        
        Pageable pageable = PageRequest.of(page, size, Sort.by(Sort.Direction.DESC, "createdAt"));
        Page<Customer> customers = customerService.searchCustomers(name, phone, level, pageable);
        
        return ResponseEntity.ok(ApiResponse.success(customers));
    }

    /**
     * 查询单个客户
     *
     * @param id 客户编号
     * @return 客户信息
     */
    @GetMapping("/{id}")
    public ResponseEntity<ApiResponse<Customer>> getCustomer(@PathVariable Long id) {
        Customer customer = customerService.getCustomerById(id);
        
        if (customer == null) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(ApiResponse.error(404, "客户不存在"));
        }
        
        return ResponseEntity.ok(ApiResponse.success(customer));
    }

    /**
     * 创建新客户
     *
     * @param customer 客户信息
     * @return 创建后的客户
     */
    @PostMapping
    public ResponseEntity<ApiResponse<Customer>> createCustomer(@RequestBody Customer customer) {
        Customer created = customerService.createCustomer(customer);
        
        return ResponseEntity.status(HttpStatus.CREATED)
                .body(ApiResponse.success(201, "创建成功", created));
    }

    /**
     * 更新客户信息
     *
     * @param id       客户编号
     * @param customer 更新的客户信息
     * @return 更新后的客户
     */
    @PutMapping("/{id}")
    public ResponseEntity<ApiResponse<Customer>> updateCustomer(
            @PathVariable Long id,
            @RequestBody Customer customer) {
        
        try {
            Customer updated = customerService.updateCustomer(id, customer);
            return ResponseEntity.ok(ApiResponse.success("更新成功", updated));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(ApiResponse.error(404, e.getMessage()));
        }
    }

    /**
     * 删除客户
     *
     * @param id 客户编号
     * @return 删除结果
     */
    @DeleteMapping("/{id}")
    public ResponseEntity<ApiResponse<Void>> deleteCustomer(@PathVariable Long id) {
        try {
            customerService.deleteCustomer(id);
            return ResponseEntity.ok(ApiResponse.success("删除成功", null));
        } catch (RuntimeException e) {
            return ResponseEntity.status(HttpStatus.NOT_FOUND)
                    .body(ApiResponse.error(404, e.getMessage()));
        }
    }
}