package com.example.crm.service;

import com.example.crm.entity.Customer;
import com.example.crm.repository.CustomerRepository;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.redis.core.RedisTemplate;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.concurrent.TimeUnit;

/**
 * 客户服务类
 */
@Service
@RequiredArgsConstructor
@Slf4j
public class CustomerService {

    private final CustomerRepository customerRepository;
    private final RedisTemplate<String, Object> redisTemplate;

    /**
     * 缓存键前缀
     */
    private static final String CACHE_PREFIX = "customer:";

    /**
     * 缓存过期时间（分钟）
     */
    private static final int CACHE_EXPIRE_MINUTES = 30;

    /**
     * 根据ID查询客户（带缓存）
     *
     * @param id 客户编号
     * @return 客户信息
     */
    public Customer getCustomerById(Long id) {
        String cacheKey = CACHE_PREFIX + id;
        
        // 先从缓存查询
        Customer customer = (Customer) redisTemplate.opsForValue().get(cacheKey);
        
        if (customer != null) {
            log.info("从缓存获取客户信息: id={}", id);
            return customer;
        }
        
        // 缓存未命中，从数据库查询
        customer = customerRepository.findById(id).orElse(null);
        
        if (customer != null) {
            // 将查询结果放入缓存
            redisTemplate.opsForValue().set(cacheKey, customer, CACHE_EXPIRE_MINUTES, TimeUnit.MINUTES);
            log.info("从数据库获取客户信息并缓存: id={}", id);
        }
        
        return customer;
    }

    /**
     * 创建新客户
     *
     * @param customer 客户信息
     * @return 创建后的客户
     */
    @Transactional
    public Customer createCustomer(Customer customer) {
        Customer saved = customerRepository.save(customer);
        
        // 更新缓存
        String cacheKey = CACHE_PREFIX + saved.getCustomerId();
        redisTemplate.opsForValue().set(cacheKey, saved, CACHE_EXPIRE_MINUTES, TimeUnit.MINUTES);
        
        log.info("创建客户成功: id={}, name={}", saved.getCustomerId(), saved.getName());
        return saved;
    }

    /**
     * 更新客户信息
     *
     * @param id       客户编号
     * @param customer 更新的客户信息
     * @return 更新后的客户
     */
    @Transactional
    public Customer updateCustomer(Long id, Customer customer) {
        Customer existing = customerRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("客户不存在: id=" + id));
        
        // 更新字段
        if (customer.getName() != null) {
            existing.setName(customer.getName());
        }
        if (customer.getPhone() != null) {
            existing.setPhone(customer.getPhone());
        }
        if (customer.getEmail() != null) {
            existing.setEmail(customer.getEmail());
        }
        if (customer.getLevel() != null) {
            existing.setLevel(customer.getLevel());
        }
        
        Customer updated = customerRepository.save(existing);
        
        // 更新缓存
        String cacheKey = CACHE_PREFIX + id;
        redisTemplate.opsForValue().set(cacheKey, updated, CACHE_EXPIRE_MINUTES, TimeUnit.MINUTES);
        
        log.info("更新客户成功: id={}", id);
        return updated;
    }

    /**
     * 删除客户（软删除）
     *
     * @param id 客户编号
     */
    @Transactional
    public void deleteCustomer(Long id) {
        if (!customerRepository.existsById(id)) {
            throw new RuntimeException("客户不存在: id=" + id);
        }
        
        customerRepository.deleteById(id);
        
        // 删除缓存
        String cacheKey = CACHE_PREFIX + id;
        redisTemplate.delete(cacheKey);
        
        log.info("删除客户成功: id={}", id);
    }

    /**
     * 分页查询客户列表
     *
     * @param name  客户姓名（可选）
     * @param phone 联系电话（可选）
     * @param level 客户等级（可选）
     * @param pageable 分页参数
     * @return 客户分页列表
     */
    public Page<Customer> searchCustomers(String name, String phone, String level, Pageable pageable) {
        return customerRepository.searchCustomers(name, phone, level, pageable);
    }
}